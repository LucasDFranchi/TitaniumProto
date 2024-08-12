template_cpp_string = """/**
 * @file {{ package_name }}Protobuf.h
 * @brief Auto-generated header file generated.
 */

#ifndef {{ package_name | upper }}_PROTO_H
#define {{ package_name | upper }}_PROTO_H

#include "stdint.h"
#include "string.h"
{%- if proto.json_enable %}
#include "{{ proto.json_path }}ArduinoJson.h"
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
        if (out_buffer == nullptr) {
            return 0;
        }

        uint16_t serialized_size = {{ proto.serialized_size }};

        if (out_buffer_size < serialized_size) {
            return 0;
        }

        uint16_t offset = 0;
{% for field in fields -%}
{%- if field.is_array %}
        memcpy(&out_buffer[offset], this->{{ field.internal_name }}, strlen(this->{{ field.internal_name }}) + 1);
{%- if not loop.last %}
        offset += strlen(this->{{ field.internal_name }}) + 1;
{%- endif %}
{%- else %}
        memcpy(&out_buffer[offset], &this->{{ field.internal_name }}, sizeof(this->{{ field.internal_name }}));
{%- if not loop.last %}
        offset += sizeof(this->{{ field.internal_name }});
{%- endif %}
{%- endif %}
{%- endfor %}

        return serialized_size;
    }

    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {
        if (in_buffer == nullptr) {
            return -1;
        }

        uint16_t deserialized_min_size = {{ proto.minimum_size }};

        if (in_buffer_size < deserialized_min_size) {
            return -3;
        }
{%- for field in fields %}
{%- if field.is_array %}
        memset(this->{{ field.internal_name }}, 0, {{ field.defined_size }});
{%- endif %}
{%- endfor %}

        uint16_t offset = 0;

{%- for field in fields %}
{%- if field.is_array %}
        memcpy(this->{{ field.internal_name }}, &in_buffer[offset], strlen(&in_buffer[offset]) + 1);
{%- if not loop.last %}
        offset += strlen(&in_buffer[offset]) + 1;
{%- endif %}
{%- else %}
        memcpy(&this->{{ field.internal_name }}, &in_buffer[offset], sizeof(this->{{ field.internal_name }}));
{%- if not loop.last %}
        offset += sizeof(this->{{ field.internal_name }});
{%- endif %}
{%- endif %}
{%- endfor %}

        return 0;
    }
{% if proto.json_enable %}
    int32_t SerializeJson(char* out_buffer, uint16_t out_buffer_size) {
        uint32_t response_length = 0;

        do {
            if (out_buffer == nullptr) {
                break;
            }

            StaticJsonDocument<{{ proto.json_size }}> doc;
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
            
            StaticJsonDocument<{{ proto.json_size }}> doc;
            
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