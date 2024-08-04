import json

from jinja2 import Template

from .titanium_field import TitaniumField

template_string = """/**
 * @file {{ package_name }}Protobuf.h
 * @brief Auto-generated header file generated.
 */

#ifndef {{ package_name | upper }}_PROTO_H
#define {{ package_name | upper }}_PROTO_H

#include "stdint.h"
#include "string.h"
{%- if proto.json_enable %}
#include "ArduinoJson.h"
{%- endif %}
#include "IProtobuf.h"

class {{ package_name }}Protobuf : public IProtobuf {
public:
    {{ package_name }}Protobuf() = default;
    ~{{ package_name }}Protobuf() = default;
{% for field in fields %}
{%- if field.is_array %}
    static constexpr uint16_t {{ field.defined_size }} = {{ field.size }};
{%- endif %}
{%- endfor %}
{% for field in fields %}
{%- if field.is_array %}
    const {{ field.c_type_name }}* Get{{ field.capitalized_name }}(void) const { return this->{{ field.internal_name }}; }
{%- else %}
    {{ field.c_type_name }} Get{{ field.capitalized_name }}(void) const { return this->{{ field.internal_name }}; }
{%- endif %}
{%- endfor %}

    int16_t GetSerializedSize(void) const {
        return ({{ proto.serialized_size }});
    }

    int16_t GetMaxSize(void) const {
        return ({{ proto.maximum_size }});
    }

    static int16_t GetStaticMaxSize(void) {
        return ({{ proto.static_maximum_size }});
    }
{% for field in fields -%}
{%- if field.is_array %}
    int8_t Update{{ field.capitalized_name }}(const {{ field.c_type_name }}* value) {
        if (value == nullptr) {
            return PROTO_INVAL_PTR;
        }

        size_t value_length = strlen(value) + 1;

        if ((value_length == 1) || {{ field.defined_size }} == 0) {
            return PROTO_OVERFLOW;
        }

        if (value_length > {{ field.defined_size }}) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->{{ field.internal_name }}, 0, {{ field.defined_size }});
        memcpy(this->{{ field.internal_name }}, value, value_length);

        return PROTO_NO_ERROR;
    }

    int8_t Update{{ field.capitalized_name }}(const {{ field.c_type_name }}* value, uint16_t string_size) {
        if (value == nullptr) {
            return PROTO_INVAL_PTR;
        }

        if ({{ field.defined_size }} == 0) {
            return PROTO_OVERFLOW;
        }

        if (string_size > {{ field.defined_size }}) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->{{ field.internal_name }}, 0, {{ field.defined_size }});
        memcpy(this->{{ field.internal_name }}, value, string_size);

        return PROTO_NO_ERROR;
    }
{% else %}
    int8_t Update{{ field.capitalized_name }}({{  field.c_type_name }} value) {
        this->{{ field.internal_name }} = value;
        return PROTO_NO_ERROR;
    }
{% endif -%}
{% endfor %}
    int16_t Serialize(char* out_buffer, uint16_t out_buffer_size) const {
        uint16_t data_position = 0;
        if (out_buffer == nullptr) {
            return 0;
        }

        uint16_t serialized_size = {{ proto.serialized_size }};

        if (out_buffer_size < serialized_size) {
            return 0;
        }  
{% for field in fields -%}
    {%- if field.c_type_name in ['uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'int8_t', 'int16_t', 'int32_t', 'int64_t'] %}
        out_buffer[data_position++] = sizeof(this->{{ field.internal_name }});
        memcpy(&out_buffer[data_position], &this->{{ field.internal_name }}, sizeof(this->{{ field.internal_name }}));
        data_position += sizeof(this->{{ field.internal_name }});
    {%- elif field.c_type_name == 'char' %}
        uint8_t length = strlen(this->{{ field.internal_name }});
        out_buffer[data_position++] = length;
        memcpy(&out_buffer[data_position], this->{{ field.internal_name }}, length);
        data_position += length;
    {%- endif %}
{% endfor %}
        return serialized_size;
    }

    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {
        uint16_t data_position = 0;
        uint8_t size = 0;
                
        if (in_buffer == nullptr) {
            return PROTO_INVAL_PTR;
        }

        uint16_t deserialized_min_size = {{ proto.minimum_size }};

        if (in_buffer_size < deserialized_min_size) {
            return PROTO_INVAL_SIZE;
        }
{% for field in fields -%}
{%- if field.is_array %}
        memset(this->{{ field.internal_name }}, 0, {{ field.defined_size }});
{%- endif -%}
{%- endfor %}
{% for field in fields -%}
    {% if field.c_type_name in ['uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'int8_t', 'int16_t', 'int32_t', 'int64_t', ] %}
        size = in_buffer[data_position++];
        if (size + data_position > in_buffer_size) return 0;
        memcpy(&this->{{ field.internal_name }}, &in_buffer[data_position], size);
        data_position += size;
    {% elif field.c_type_name == 'char' %}
        uint8_t length = in_buffer[data_position++];
        if (length + data_position > in_buffer_size) return 0;
        memcpy(this->{{ field.internal_name }}, &in_buffer[data_position], length);
        this->{{ field.internal_name }}[length] = '\\0';
        data_position += length;
    {%- endif %}
{%- endfor %}
        return PROTO_NO_ERROR;
    }
{% if proto.json_enable %}
    int32_t SerializeJson(char* out_buffer, uint16_t out_buffer_size) {
        uint32_t response_length = 0;

        do {
            if (out_buffer == nullptr) {
                break;
            }

            StaticJsonDocument<512> doc;
{%- for field in fields %}         
            doc["{{ field.token_name }}"] = this->{{ field.internal_name }};
{%- endfor %}
            response_length = serializeJson(doc, out_buffer, out_buffer_size);
        } while (0);

        return response_length;
    }

    int8_t DeSerializeJson(const char* in_buffer, uint16_t in_buffer_size) {
        auto result = PROTO_NO_ERROR;

        do {
            if (in_buffer == nullptr) {
                result = PROTO_INVAL_PTR;
                break;
            }
            
            StaticJsonDocument<512> doc;
            
            if (deserializeJson(doc, in_buffer)) {
                result = PROTO_INVAL_JSON_PARSE;
                break;
            }
{%- for field in fields %}
            if (!doc.containsKey("{{ field.token_name }}")) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }
{%- endfor %}
{%- for field in fields %}
            if (this->Update{{ field.capitalized_name }}(doc["{{ field.token_name }}"])) {
                result = PROTO_INVAL_JSON_VALUE;
                break;
            }
{%- endfor %}

            result = PROTO_NO_ERROR;

        } while(0);

        return result;
    }
{%- endif %}

private:
{%- for field in fields %}
    {{ field.c_type_name }} {{ field.internal_name }}{% if field.is_array %}[{{ field.size }}] = {0}{%- else %} = 0{% endif %};
{%- endfor %}
};
#endif /* {{ package_name | upper }}_PROTO_H */

"""

class TitaniumFileGenerator:
    _SUPPORTED_TYPES = [
        "uint8_t",
        "int8_t",
        "uint16_t",
        "int16_t",
        "uint32_t",
        "int32_t",
        "uint64_t",
        "int64_t",
        "float",
        "double",
        "string",
    ]

    def __init__(self):
        """
        Initializes a new instance of the TitaniumProto class.
        """
        self._content = None
        self._package_name = None
        self._fields = []

        self._template = Template(template_string)

    def _read_file(self, filepath: str):
        """
        Read content from a JSON file.

        Args:
            filepath (str): Path to the Titanium Protobuf JSON file.
        """
        with open(filepath, "r") as file:
            self._content = json.load(file)

    def _update_package_name(self):
        """
        Updates the package name by parsing the protocol file content.

        Raises:
            ValueError: If the package name is missing.
        """
        self._package_name = self._content.get("package")
        if self._package_name is None:
            raise ValueError("Missing Package Name in protocol file.")

    def _parse_fields(self):
        """
        Parse and validate fields from the protocol file content.

        Raises:
            ValueError: If a field has an unsupported data type.
        """
        token_id = 1
        for field in self._content.get("fields"):
            field_type = field.get("type")
            field["token_id"] = token_id
            if field_type not in self._SUPPORTED_TYPES:
                supported_types_str = ", ".join(self._SUPPORTED_TYPES)
                raise ValueError(
                    f"Unsupported data type: {field_type}. Supported types are: {supported_types_str}."
                )

            self._fields.append(TitaniumField(field))
            token_id += 2

    def import_and_parse_proto_file(self, filepath: str = None, raw_data: str = None):
        """
        Imports and parses definitions from a Titanium protobuf file.

        Args:
            filepath (str): Path to the Titanium protobuf file.
        
        Raises:
            ValueError: If there are syntax errors in the protobuf file or required fields are missing.
        """
        if filepath:
            self._read_file(filepath)
        else:
            self._content = raw_data

        self._update_package_name()
        self._parse_fields()
        
    def generate_header_file(self, redirect_outfile: str = "", enable_json: bool = False, jsmn_path: str = ""):
        data = {}
        serialized_size_list = []
        maximum_size_list = []
        minimum_size_list = []
        static_maximum_size_list = []
        num_of_arrays = 0
        
        data["package_name"] = self._package_name
        data["fields"] = []
        for field in self._fields:
            data["fields"].append(field.to_dict())
            
            if field.is_array:
                serialized_size_list.append(f"strlen(this->{field.internal_name})")
                static_maximum_size_list.append(f"{field.defined_size}")
                num_of_arrays += 1
            else:
                serialized_size_list.append(f"sizeof(this->{field.internal_name})")
                static_maximum_size_list.append(f"sizeof({field.type_name})")
                minimum_size_list.append(f"sizeof(this->{field.internal_name})")
                
            maximum_size_list.append(f"sizeof(this->{field.internal_name})")

        data["proto"] = {}            
        data["proto"]["serialized_size"] =  " + ".join(serialized_size_list) + f" + {len(self._fields)}"
        data["proto"]["maximum_size"] = " + ".join(maximum_size_list)
        data["proto"]["minimum_size"] = " + ".join(minimum_size_list) + f" + {num_of_arrays}"
        data["proto"]["static_maximum_size"] = " + ".join(static_maximum_size_list)
        data["proto"]["num_tokens"] = (len(self._fields) * 2) + 1
        data["proto"]["json_enable"] = enable_json
        data["proto"]["jsmn_path"] = jsmn_path
        data["proto"]["num_var"] = len(self._fields)
        
        rendered_code = self._template.render(data)
        
        with open(f"{redirect_outfile}{self._package_name}Proto.h", 'w') as file:
            file.write(rendered_code)