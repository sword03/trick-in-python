import json

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'repr_json'):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)

class JsonObject(object):
    def repr_json(self):
        return NotImplementedError(JsonObject.repr_json)

    def to_json(self):
        return json.dumps(self, cls=ComplexEncoder)

    @classmethod
    def from_json(cls, json_str):
        jo = json.loads(json_str)
        return cls(jo)

class StrObject(object):
    '''
    Show object like this(Support embeded object):
    sw = SimpleWallet(...)
    print(sw)

        [SimpleWallet]
        address_type:0
        address:2N1xvuhNX8xxQWHAqmtgDREVsHiWfeBfm8s
        key_pairs:
            [KeyPairEx]
                public_key:0347ceaa76974fde3864bb1e92bbc8e7327f9a9cc11b496bfb17660d98d99c6ad3
                private_key:cQm9eufpHbpDUVCFStpHuiYdXU3CfJXCxD1VtaENfiKR7PuQqaCw
            [KeyPairEx]
                public_key:0207d3c7276f25645e7aca467b5a579b92c3e20b6ae2bcc720a151afb873edf89f
                private_key:cQLDDJXTdsUmx1E6k6gmba2DruBdjwz82MrNXb3YDa5ifaN9W7sp
        required:2
        sort_public_key:True

    '''
    def repr_str(self, extra_tab=0):
        def tab(count):
            return " " * 8 * count

        def to_str(value):
            if isinstance(value, list):
                return ''.join(item.repr_str(extra_tab+1) for item in value)
            else:
                return value

        # head
        s = '\n' + tab(extra_tab) +'[' + type(self).__name__ + ']\n'
        # content
        layout = tab(extra_tab) + '    {0}:{1}'
        s += '\n'.join(layout.format(key, to_str(value))
                       for key, value in self.__dict__.items())
        return s

    def __str__(self):
        return self.repr_str()


class KeyPairEx(JsonObject, StrObject):
    """
    Will contain the input of a transaction.
    @type public_key: String
    @type private_key: String
    """
    def __init__(self, parsed_json):
        self.kp_index = parsed_json["kp_index"]
        self.public_key = parsed_json["public_key"]
        self.private_key = parsed_json["private_key"]

    def repr_json(self):
        return dict(kp_index=self.kp_index, public_key=self.public_key, private_key=self.private_key)

class MultiSigWallet(JsonObject, StrObject):
    """
    Will contain the input of a transaction.
    @type address_type: String
    @type address: String
    @type key_pairs: KeyPairEx
    @type required: int
    @type sort_public_key: bool
    """
    def __init__(self, parsed_json):
        self.address_type = parsed_json["address_type"]
        self.address = parsed_json["address"]
        self.key_pairs = []
        for kp in parsed_json["key_pairs"]:
            self.key_pairs.append(KeyPairEx(kp))
        self.required = parsed_json["required"]
        self.sort_public_key = parsed_json["sort_public_key"]

    def repr_json(self):
        return dict(address_type=self.address_type,
                    address=self.address,
                    key_pairs=self.key_pairs,
                    required=self.required,
                    sort_public_key=self.sort_public_key)

class SimpleWallet(JsonObject, StrObject):
    """
    Will contain the input of a transaction.
    @type address_type: String
    @type address: String
    @type key_pairs: KeyPairEx
    @type required: int
    @type sort_public_key: bool
    """
    def __init__(self, parsed_json):
        self.address_type = parsed_json["address_type"]
        self.address = parsed_json["address"]
        self.key_pair = KeyPairEx(parsed_json["key_pair"])

    def repr_json(self):
        return dict(address_type=self.address_type,
                    address=self.address,
                    key_pairs=self.key_pair)

class Interval(JsonObject, StrObject):
    """
    Will contain the input of a transaction.
    @type public_key: String
    @type private_key: String
    """
    def __init__(self, parsed_json):
        self.interval_index = parsed_json["interval_index"]
        self.start = parsed_json["start"]
        self.end = parsed_json["end"]

    def repr_json(self):
        return dict(start=self.start, end=self.end)


class PoolAllocation(JsonObject, StrObject):
    """
    Will contain the info of a pool allocation.
    @type enterprise_id: String
 ,
                    required=self.required,
                    sort_public_key=self.sort_public_key   @type interval_list: Interval
    @type current_pos: int
    """
    def __init__(self, parsed_json):
        self.enterprise_id = parsed_json["enterprise_id"]
        self.interval_list = parsed_json["interval_list"]
        self.current_pos = parsed_json["current_pos"]

    def add_interval(self, interval):
        self.interval_list.append(interval)

    def get_num_of_interval(self):
        return len(self.interval_list)

    def repr_json(self):
        return dict(enterprise_id=self.enterprise_id,
                    interval_list=self.interval_list,
                    current_pos=self.current_pos)


class PoolInfo(JsonObject, StrObject):
    """
    Will contain the info of a key pair pool.
    @type pool_name: String
    @type pool_size: int, pool size is the quantity of the interval
    @type interval_size: int
    @type timestamp: int, pool size is the quantity of the interval used
    """
    def __init__(self, parsed_json):
        self.pool_name = parsed_json["pool_name"]
        self.pool_size = parsed_json["pool_size"]
        self.interval_size = parsed_json["enterprise_id"]
        self.used_size = parsed_json["used_size"]
        self.timestamp = parsed_json["timestamp"]

    def get_an_interval_unused(self):
        start = self.interval_size * self.used_size
        end = start + self.interval_size
        return Interval({
            'interval_index': self.interval_size,
            'start': start,
            'end': end
        })

    def get_num_of_interval_unused(self):
        return self.pool_size - self.used_size

    def repr_json(self):
        return dict(pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    interval_size=self.interval_size,
                    used_size=self.used_size,
                    timestamp=self.timestamp)

if __name__ == "__main__":
    jo = {
        'address_type':
        0,
        'address':
        '2N1xvuhNX8xxQWHAqmtgDREVsHiWfeBfm8s',
        'key_pairs': [{
            'kp_index': 0,
            'public_key':
            '0347ceaa76974fde3864bb1e92bbc8e7327f9a9cc11b496bfb17660d98d99c6ad3',
            'private_key':
            'cQm9eufpHbpDUVCFStpHuiYdXU3CfJXCxD1VtaENfiKR7PuQqaCw'
        }, {
            'kp_index': 1,
            'public_key':
            '0207d3c7276f25645e7aca467b5a579b92c3e20b6ae2bcc720a151afb873edf89f',
            'private_key':
            'cQLDDJXTdsUmx1E6k6gmba2DruBdjwz82MrNXb3YDa5ifaN9W7sp'
        }],
        'required':
        2,
        'sort_public_key':
        True
    }
    js = json.dumps(jo)
    '''
    print(js)
    sw = SimpleWallet(jo)
    js = json.dumps(sw, cls=ComplexEncoder)
    print(js)
    '''
    mw = MultiSigWallet.from_json(js)
    json_str = mw.to_json()
    assert isinstance(json_str, str)
    print(json_str)
    print(mw)
    print(str(mw.key_pairs[0]))
