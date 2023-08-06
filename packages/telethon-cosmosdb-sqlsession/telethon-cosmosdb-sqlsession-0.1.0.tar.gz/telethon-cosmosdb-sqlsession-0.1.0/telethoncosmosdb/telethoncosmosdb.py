import datetime

from azure.cosmos import CosmosClient, PartitionKey
from datetime import datetime
import json
from telethon import utils
from telethon.tl import types
from telethon.crypto import AuthKey
from telethon.sessions.memory import MemorySession, _SentFileType
from telethon.tl.types import InputPhoto, InputDocument, PeerUser, PeerChat, PeerChannel


class CosmosDBSQLSession(MemorySession):
    
    def __init__(self, session_name, endpoint, key, database_name, **kwargs):
        super().__init__()
        self.save_entities = True
        self.endpoint = endpoint
        self.key = key
        self.database_name = database_name
        self.session_name = session_name
        
        # Get Cosmos DB client
        self.cosmos_client = CosmosClient(self.endpoint, self.key, **kwargs)
        self.cosmosdb = self.cosmos_client.create_database_if_not_exists(self.database_name)
        
        # Look for existing session
        session_container = self.get_session_container()
        query = 'SELECT * FROM c'
        for item in session_container.query_items(query, enable_cross_partition_query=True):
            self._dc_id = item['dc_id']
            self._server_address = item['server_address']
            self._port = item['port']
            self._takeout_id = item['takeout_id']
            self._auth_key = AuthKey(
                data=self.intlist_to_byte(item['auth_key']))
            break
    
    # telethon_entity = {
        # id,
        # hash,
        # username,
        # phone,
        # name     
    # }
    def get_entity_container(self):
        partition_key = PartitionKey('/id')
        return self.cosmosdb.create_container_if_not_exists(
            id='telethon_entity_{}'.format(self.session_name), partition_key=partition_key)
    
    # telethon_sent_file {
        # id,
        # md5_digest,
        # file_size,
        # type,
        # hash
    # }
    def get_sent_file_container(self):
        partition_key = PartitionKey('/id')
        return self.cosmosdb.create_container_if_not_exists(
            id='telethon_sent_file_{}'.format(self.session_name), partition_key=partition_key)
        
    # telethon_session {
        # dc_id,
        # server_address,
        # port,
        # auth_key, 
        # takeout_id
    # }
    def get_session_container(self):
        partition_key = PartitionKey('/dc_id')
        return self.cosmosdb.create_container_if_not_exists(
            id='telethon_session_{}'.format(self.session_name), partition_key=partition_key)
        
    # telethon_updatestate {
        # id,
        # pts,
        # qts,
        # date,
        # seq
    # }
    def get_updatestate_container(self):
        partition_key = PartitionKey('/dc_id')
        return self.cosmosdb.create_container_if_not_exists(
            id='telethon_updatestate_{}'.format(self.session_name), partition_key=partition_key)
        
    # telethon_version {
        # version    
    # }
    def get_version_container(self):
        partition_key = PartitionKey('/version')
        return self.cosmosdb.create_container_if_not_exists(
            id='telethon_version_{}'.format(self.session_name), partition_key=partition_key)
        

    def set_dc(self, dc_id, server_address, port):
        super().set_dc(dc_id, server_address, port)
        self._update_session_table()

        session_container = self.get_session_container()
        query = 'SELECT * FROM c'
        
        for item in session_container.query_items(query, enable_cross_partition_query=True):
            if item and item['auth_key']:
                self._auth_key = AuthKey(
                    data=self.intlist_to_byte(item['auth_key']))
            else:
                self._auth_key = None
            break
        
    @MemorySession.auth_key.setter
    def auth_key(self, value):
        self._auth_key = value
        self._update_session_table()

    @MemorySession.takeout_id.setter
    def takeout_id(self, value):
        self._takeout_id = value
        self._update_session_table()
        

    @staticmethod
    def int_to_bytes(number: int) -> bytes:
        return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)

    @staticmethod
    def int_from_bytes(binary_data: bytes) -> int:
        return int.from_bytes(binary_data, byteorder='big', signed=True)
    
    @staticmethod
    def bytes_to_intlist(binary_data):
        intlist = []
        for byte in binary_data:
            intlist.append(byte)
        return intlist
    
    @staticmethod
    def intlist_to_byte(intlist):
        if len(intlist) == 0: return b''
        
        return bytes(intlist)
        
    def _update_session_table(self):
        session_container = self.get_session_container()
        query = 'SELECT * FROM c'
        
        for item in session_container.query_items(query, enable_cross_partition_query=True):
            session_container.delete_item(item, item['dc_id'])
        
        item = {
            'dc_id': str(self._dc_id),
            'server_address': self._server_address,
            'port': self._port,
            #'auth_key': self._auth_key.key if self._auth_key else '',
            'auth_key': self.bytes_to_intlist(self._auth_key.key) if self._auth_key else self.bytes_to_intlist(b''),
            'takeout_id': self._takeout_id
        }
        
        session_container.upsert_item(json.loads(json.dumps(item)))
        
    def get_update_state(self, entity_id):
        updatestate_container = self.get_updatestate_container()
        query = 'SELECT * FROM c where c.id = {}'.format(entity_id)
        
        for item in updatestate_container.query_items(query, enable_cross_partition_query=True):
            item_timestamp = datetime.fromisoformat()(item['date'], tz=datetime.timezone.utc)
            return types.updates.State(item['pts'], item['qts'], item_timestamp, item['seq'], unread_count=0)


    def set_update_state(self, entity_id, state):
        item = {
            'entity_id': str(entity_id),
            'pts': state.pts,
            'qts': state.qts,
            'date': state.date.isoformat(),
            'seq': state.seq()
        }
        updatestate_container = self.get_updatestate_container()
        updatestate_container.upsert_item(json.loads(json.dumps(item)))
        
    def save(self):
        pass

    def close(self):
        pass
    
    def delete(self):
        session_container = self.get_session_container()
        query = 'SELECT * FROM c'
        
        for item in session_container.query_items(query, enable_cross_partition_query=True):
            session_container.delete_item(item, item['dc_id'])
            break

    # @classmethod
    # def list_sessions(cls):
    #     session_container = self.get_session_container()
    #     sessions = []
    #     query = 'SELECT * FROM c'
        
    #     for item in session_container.query_items(query):
    #         sessions.append(item)
        
    #     return sessions

    def process_entities(self, tlo):
        
        if not self.save_entities:
            return
        
        rows = self._entities_to_rows(tlo)
        if not rows:
            return
        
        entity_container = self.get_entity_container()
        
        for row in rows:
            item = {
                'id': str(row[0]),
                'hash': row[1],
                'username': row[2],
                'phone': row[3],
                'name': row[4]
            }
            entity_container.upsert_item(json.loads(json.dumps(item)))
        
    def get_entity_from_container(self, query):
        entity_container = self.get_entity_container()
        
        items = []
        for item in entity_container.query_items(query, enable_cross_partition_query = True):
            items.append(item)
        
        return items
    
    def get_entity_rows_by_phone(self, phone):
        query = "SELECT * FROM c WHERE c.phone = {}".format(phone)
        return self.get_entity_from_container(query)
    
    def get_entity_rows_by_username(self, username):
        query = "SELECT * FROM c WHERE c.username = {}".format(username)
        return self.get_entity_from_container(query)

    def get_entity_rows_by_name(self, name):
        query = "SELECT * FROM c WHERE c.name = {}".format(name)
        return self.get_entity_from_container(query)
    
    def get_entity_rows_by_id(self, id, exact=True):
        if exact:
            query = "SELECT * FROM c WHERE c.id = {}".format(id)
        else:
            query = "SELECT * FROM c WHERE c.id in ({}, {}, {})".format(
                utils.get_peer_id(PeerUser(id)), 
                utils.get_peer_id(PeerChat(id)),
                utils.get_peer_id(PeerChannel(id))
                )
        return self.get_entity_from_container(query)
            
    def get_file(self, md5_digest, file_size, cls):
        sentfile_container = self.get_sent_file_container()
        
        query = "SELECT * FROM c WHERE c.md5_digest='{}' AND c.file_size={} AND c.type='{}'".format(
            md5_digest, file_size, _SentFileType.from_type(cls).value
        )
        
        for item in sentfile_container.query_items(query, enable_cross_partition_query=True):
            return item['id'], item['hash']

    def cache_file(self, md5_digest, file_size, instance):
        
        if not isinstance(instance, (InputDocument, InputPhoto)):
            raise TypeError('Cannot cache %s instance' % type(instance))
        
        sentfile_container = self.get_sent_file_container()
            
        item = {
            'md5_digest': md5_digest,
            'file_size': file_size,
            'type': _SentFileType.from_type(type(instance)).value,
            'id': str(instance.id),
            'hash': instance.access_hash
        }
        
        sentfile_container.upsert_item(json.loads(json.dumps(item)))
    
    def clone(self, to_instance=None):
        cloned = super().clone(to_instance)
        cloned.save_entities = self.save_entities
        return cloned
        
