import redis

_RR_REDIS_POOL = None


def set_connection_param(host, port, db, password):
    global _RR_REDIS_POOL
    _RR_REDIS_POOL = redis.ConnectionPool(host=host,
                                          port=port,
                                          db=db,
                                          password=password)


def _get_connection():
    """TODO: Docstring for CreateClient.
    :returns: TODO

    """
    redis_conn = redis.Redis(connection_pool=_RR_REDIS_POOL)
    return redis_conn


class RStr(object):
    """Implement by "key-hash table" in redis"""
    def __init__(self):
        """TODO: to be defined1. """
    @classmethod
    def set(cls, k, data):
        """TODO: Docstring for set.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.set(k, data)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def get(cls, k):
        """TODO: Docstring for get.
        """
        try:
            redis_conn = _get_connection()
            res = redis_conn.get(k)
            if res is None:
                return None
            content = res.decode()
            return content
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def remove(cls, k):
        """TODO: Docstring for remove.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.hdel(k)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def exists(cls, k):
        """TODO: Docstring for exists.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.hexists(k)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e


class RHashTable(object):
    """Implement by "key-hash table" in redis"""
    def __init__(self):
        """TODO: to be defined1. """
    @classmethod
    def set(cls, key, k, data):
        """TODO: Docstring for set.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.hset(key, k, data)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e
    @classmethod

    def set_batch(cls, key, k_data_tuple_list):
        """TODO: Docstring for set.
        k_data_tuple_list means:
            [(k1,data1),(k2,data2)....(kn,datan)]
        """
        try:
            redis_conn = _get_connection()
            pip = redis_conn.pipeline()
            for item in k_data_tuple_list:
                k = item(0)
                data = item(1)
                pip.hset(key, k, data)
            return pip.execute()
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def get(cls, key, k):
        """TODO: Docstring for get.
        """
        try:
            redis_conn = _get_connection()
            res = redis_conn.hget(key, k)
            if res is None:
                return None
            content = res.decode()
            return content
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def get_all(cls, key):
        """TODO: Docstring for get_all.
        """
        try:
            redis_conn = _get_connection()
            res = redis_conn.hgetall(key)
            addr_array = []
            for k, v in res.items():
                content = v.decode()
                addr_array.append(content)
            return addr_array
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def remove(cls, key, k):
        """TODO: Docstring for remove.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.hdel(key, k)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def count(cls, key):
        """TODO: Docstring for count.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.hlen(key)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e

    @classmethod
    def exists(cls, key, k):
        """TODO: Docstring for exists.
        """
        try:
            redis_conn = _get_connection()
            return redis_conn.hexists(key, k)
        except redis.RedisError as e:
            print('redis exception: {0}'.format(e))
            raise e


if __name__ == "__main__":
    set_connection_param(host='localhost', port=6379 , db=0, password='foobared')
    RStr.set('hello', 'world1234')
    d = RStr.get('hello')
    RHashTable.set('hellot', 1, 'world1234')
    d = RHashTable.get('hellot', 1)
    print(d)

