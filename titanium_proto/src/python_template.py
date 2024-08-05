template_python_string = """import json
import struct

class TestProtobuf:
{% for field in fields %}
{%- if field.is_array %}
    {{ field.defined_size }} = {{ field.size }}
{%- endif %}
{%- endfor %}
    PROTO_NO_ERROR = 0
    PROTO_INVAL_PTR = -1
    PROTO_OVERFLOW = -2
    PROTO_INVAL_SIZE = -3
    PROTO_INVAL_JSON_PARSE = -4
    PROTO_INVAL_JSON_KEY = -5
    PROTO_INVAL_JSON_VALUE = -6

    def __init__(self):
{%- for field in fields %}
{%- if field.is_array %}
        self.{{ field.internal_name }} = ""
{%- else %}
        self.{{ field.internal_name }} = 0
{%- endif %}
{%- endfor %}
{% for field in fields %}
    def get_{{ field.token_name }}(self):
        return self.{{ field.internal_name }}
{% endfor %}
{%- for field in fields %}
    def update_{{ field.token_name }}(self, value):
{%- if field.is_array %}
        if value is None:
            return self.PROTO_INVAL_PTR
        value_length = len(value)
        if value_length == 0 or self.{{ field.defined_size }} == 0:
            return self.PROTO_OVERFLOW
        if value_length > self.{{ field.defined_size }}:
            return self.PROTO_INVAL_SIZE
        self._fourth_field = value
        return self.PROTO_NO_ERROR
{%- else %}
        self.{{ field.internal_name }} = value
        return self.PROTO_NO_ERROR
{%- endif %}
{% endfor %}
    def serialize(self, out_buffer):
        if out_buffer is None:
            return 0

        data_position = 0
{% for field in fields %}
{%- if field.is_array %}
        length = len(self.{{ field.internal_name }})
        out_buffer[data_position] = length
        data_position += 1
        out_buffer[data_position:data_position + length] = self.{{ field.internal_name }}.encode('utf-8')
        data_position += length
{% else %}
        out_buffer[data_position] = struct.pack('{{ field.c_to_struct }}', struct.calcsize('{{ field.c_to_struct }}'))[0]
        data_position += 1
        struct.pack_into('{{ field.c_to_struct }}', out_buffer, data_position, self.{{ field.internal_name }})
        data_position += struct.calcsize('{{ field.c_to_struct }}')
{% endif %}
{%- endfor %}
        return data_position

    def deserialize(self, data):
        try:
            data_position = 0
{% for field in fields %}
{%- if field.is_array %}
            self.{{ field.token_name }}_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self._fourth_field = struct.unpack_from(
                '{}s'.format(self.{{ field.token_name }}_size),
                data,
                data_position
            )[0].decode('utf-8')
            data_position += self.{{ field.token_name }}_size
{% else %}
            self.{{ field.token_name }}_size = struct.unpack_from('B', data, data_position)[0]
            data_position += 1
            self.{{ field.internal_name }} = struct.unpack_from('{{ field.c_to_struct }}', data, data_position)[0]
            data_position += self.{{ field.token_name }}_size
{% endif %}
{%- endfor %}
            return self.PROTO_NO_ERROR
        except Exception:
            return self.PROTO_INVAL_PTR

    def serialize_json(self, out_buffer, out_buffer_size):
        if out_buffer is None:
            return 0

        # Create a dictionary with the fields
        data = {
{%- for field in fields %}
            "{{ field.token_name }}": self.{{ field.internal_name }}{% if not loop.last %},{% endif %}
{%- endfor %}
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
            data = json.loads(json_str.split('\\x00')[0])

{%- for field in fields %}
            if "{{ field.token_name }}" not in data:
                return self.PROTO_INVAL_JSON_KEY
{%- endfor %}
{%- for field in fields %}
            if self.update_{{ field.token_name }}(data["{{ field.token_name }}"]) != self.PROTO_NO_ERROR:
                return self.PROTO_INVAL_JSON_VALUE
{%- endfor %}
            return self.PROTO_NO_ERROR
        except json.JSONDecodeError:
            return self.PROTO_INVAL_JSON_PARSE

"""