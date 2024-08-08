import json
import struct

class _TestProtobuf:

    FOURTH_FIELD_SIZE = 128
    PROTO_NO_ERROR = 0
    PROTO_INVAL_PTR = -1
    PROTO_OVERFLOW = -2
    PROTO_INVAL_SIZE = -3
    PROTO_INVAL_TYPE = -4
    PROTO_INVAL_JSON_PARSE = -5
    PROTO_INVAL_JSON_KEY = -6
    PROTO_INVAL_JSON_VALUE = -7

    def __init__(self):
        self._first_field = 0
        self._second_field = 0
        self._third_field = 0
        self._fourth_field = ""
        self._five_field = 0

    def get_first_field(self):
        return self._first_field

    def get_second_field(self):
        return self._second_field

    def get_third_field(self):
        return self._third_field

    def get_fourth_field(self):
        return self._fourth_field

    def get_five_field(self):
        return self._five_field

    def update_first_field(self, value):
        if isinstance(value, int):        
            self._first_field = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_second_field(self, value):
        if isinstance(value, int):        
            self._second_field = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_third_field(self, value):
        if isinstance(value, int):        
            self._third_field = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def update_fourth_field(self, value):
        if value is None:
            return self.PROTO_INVAL_PTR
        if not isinstance(value, str):
            return self.PROTO_INVAL_TYPE
        value_length = len(value)
        if value_length == 0 or self.FOURTH_FIELD_SIZE == 0:
            return self.PROTO_OVERFLOW
        if value_length > self.FOURTH_FIELD_SIZE:
            return self.PROTO_INVAL_SIZE
        self._fourth_field = value
        return self.PROTO_NO_ERROR

    def update_five_field(self, value):
        if isinstance(value, int):        
            self._five_field = value
            return self.PROTO_NO_ERROR

        return self.PROTO_INVAL_TYPE

    def serialize(self, out_buffer):
        if out_buffer is None:
            return 0

        data_position = 0

        out_buffer[data_position] = struct.pack('B', struct.calcsize('B'))[0]
        data_position += 1
        struct.pack_into('B', out_buffer, data_position, self._first_field)
        data_position += struct.calcsize('B')

        out_buffer[data_position] = struct.pack('I', struct.calcsize('I'))[0]
        data_position += 1
        struct.pack_into('I', out_buffer, data_position, self._second_field)
        data_position += struct.calcsize('I')

        out_buffer[data_position] = struct.pack('H', struct.calcsize('H'))[0]
        data_position += 1
        struct.pack_into('H', out_buffer, data_position, self._third_field)
        data_position += struct.calcsize('H')

        length = len(self._fourth_field)
        out_buffer[data_position] = length
        data_position += 1
        out_buffer[data_position:data_position + length] = self._fourth_field.encode('utf-8')
        data_position += length

        out_buffer[data_position] = struct.pack('q', struct.calcsize('q'))[0]
        data_position += 1
        struct.pack_into('q', out_buffer, data_position, self._five_field)
        data_position += struct.calcsize('q')

        return data_position

    def deserialize(self, data):
        try:
            data_position = 0

            self.first_field_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._first_field = struct.unpack_from('B', data, data_position)[0]
            data_position += self.first_field_size

            self.second_field_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._second_field = struct.unpack_from('I', data, data_position)[0]
            data_position += self.second_field_size

            self.third_field_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._third_field = struct.unpack_from('H', data, data_position)[0]
            data_position += self.third_field_size

            self.fourth_field_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._fourth_field = struct.unpack_from(
                '{}s'.format(self.fourth_field_size),
                data,
                data_position
            )[0].decode('utf-8')
            data_position += self.fourth_field_size

            self.five_field_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._five_field = struct.unpack_from('q', data, data_position)[0]
            data_position += self.five_field_size

            return self.PROTO_NO_ERROR
        except Exception:
            return self.PROTO_INVAL_PTR

    def serialize_json(self, out_buffer, out_buffer_size):
        if out_buffer is None:
            return 0

        # Create a dictionary with the fields
        data = {
            "first_field": self._first_field,
            "second_field": self._second_field,
            "third_field": self._third_field,
            "fourth_field": self._fourth_field,
            "five_field": self._five_field
        }
        json_data = json.dumps(data)

        if len(json_data) > out_buffer_size:
            return 0

        out_buffer[:len(json_data)] = json_data.encode('utf-8')

        return len(json_data)

    def deserialize_json(self, in_buffer):
        if in_buffer is None:
            return self.PROTO_INVAL_PTR

        try:
            json_str = in_buffer.decode('utf-8')
            data = json.loads(json_str.split('\x00')[0])
            if "first_field" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "second_field" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "third_field" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "fourth_field" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if "five_field" not in data:
                return self.PROTO_INVAL_JSON_KEY
            if self.update_first_field(data["first_field"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_second_field(data["second_field"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_third_field(data["third_field"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_fourth_field(data["fourth_field"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            if self.update_five_field(data["five_field"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
            return self.PROTO_NO_ERROR
        except json.JSONDecodeError:
            return self.PROTO_INVAL_JSON_PARSE
