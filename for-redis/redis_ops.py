from .redis_basic import set_connection_param, RStr, RHashTable
from .entity import PoolInfo, PoolAllocation, Interval, SimpleWallet, KeyPairEx

def init_app(app):
    global RR_REDIS_POOL
    REDIS = app.config['REDIS']
    set_connection_param(host=REDIS['host'],
                         port=REDIS['port'],
                         db=REDIS['db'],
                         password=REDIS['requirepass'])

KEY_POOL_INFO = 'rstr_pool_info'
KEY_POOL_ALLOCATION = 'htable_pool_allocation'
KEY_POOL_KEY_PAIR = 'htable_pool_key_pair'
KEY_SIMPLE_WALLET = 'htable_simple_wallet'

def exsit_pool_info():
    return RStr.exists(KEY_POOL_INFO)

def query_pool_info():
    return PoolInfo.from_json(RStr.get(KEY_POOL_INFO))

def update_pool_info(pool_info):
    return RStr.set(KEY_POOL_INFO, pool_info.to_json())

def query_pool_allocation(enterprise_id):
    return PoolAllocation.from_json(RHashTable.get(KEY_POOL_ALLOCATION, enterprise_id))

def exists_pool_allocation(enterprise_id):
    return RHashTable.exists(KEY_POOL_ALLOCATION, enterprise_id)

def query_all_pool_allocation():
    ret = []
    for pa in RHashTable.get_all(KEY_POOL_ALLOCATION):
        ret.append(PoolAllocation.from_json(pa))
    return ret

def update_pool_allocation(pool_allocation):
    return RHashTable.set(KEY_POOL_ALLOCATION, pool_allocation.to_json())

def query_key_pair(kp_index):
    return KeyPairEx.from_json(RHashTable.get(KEY_POOL_KEY_PAIR, kp_index))

def query_all_key_pairs():
    ret = []
    for kp in RHashTable.get_all(KEY_POOL_KEY_PAIR):
        ret.append(KEY_POOL_KEY_PAIR.from_json(kp))
    return ret

def insert_key_pairs_batch(kp_list):
    k_data_tuple_list = []
    for item in kp_list:
        k = item.kp_index
        data = item.to_json()
        k_data_tuple_list.append((k, data))
    RHashTable.set_batch(KEY_POOL_KEY_PAIR, k_data_tuple_list)

def update_key_pair(kp):
    return RHashTable.set(KEY_POOL_KEY_PAIR, kp.kp_index, kp.to_json())




if __name__ == "__main__":
    set_connection_param(host='localhost', port=6379 , db=0, password='foobared')
    RStr.set('hello', 'world1234')
    d = RStr.get('hello')
    RHashTable.set('hellot', 1, 'world1234')
    d = RHashTable.get('hellot', 1)
    print(d)
