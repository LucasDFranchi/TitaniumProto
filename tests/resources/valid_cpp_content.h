/**
 * @file _TestProtobuf.h
 * @brief Auto-generated header file generated.
 */

#ifndef _TEST_PROTO_H
#define _TEST_PROTO_H

#include "stdint.h"
#include "string.h"
#include "ArduinoJson.h"
#include "IProtobuf.h"

class _TestProtobuf : public IProtobuf {
public:
    _TestProtobuf() = default;
    ~_TestProtobuf() = default;

    static constexpr uint16_t FOURTH_FIELD_SIZE = 128;

    uint8_t GetFirstField(void) const { return this->_first_field; }
    uint32_t GetSecondField(void) const { return this->_second_field; }
    uint16_t GetThirdField(void) const { return this->_third_field; }
    const char* GetFourthField(void) const { return this->_fourth_field; }
    int64_t GetFiveField(void) const { return this->_five_field; }

    int16_t GetSerializedSize(void) const {
        return (sizeof(this->_first_field) + sizeof(this->_second_field) + sizeof(this->_third_field) + strlen(this->_fourth_field) + sizeof(this->_five_field));
    }

    int16_t GetMaxSize(void) const {
        return (sizeof(this->_first_field) + sizeof(this->_second_field) + sizeof(this->_third_field) + sizeof(this->_fourth_field) + sizeof(this->_five_field));
    }

    static int16_t GetStaticMaxSize(void) {
        return (sizeof(uint8_t) + sizeof(uint32_t) + sizeof(uint16_t) + FOURTH_FIELD_SIZE + sizeof(int64_t));
    }

    int8_t UpdateFirstField(uint8_t value) {
        this->_first_field = value;
        return PROTO_NO_ERROR;
    }

    int8_t UpdateSecondField(uint32_t value) {
        this->_second_field = value;
        return PROTO_NO_ERROR;
    }

    int8_t UpdateThirdField(uint16_t value) {
        this->_third_field = value;
        return PROTO_NO_ERROR;
    }

    int8_t UpdateFourthField(const char* value) {
        if (value == nullptr) {
            return PROTO_INVAL_PTR;
        }

        size_t value_length = strlen(value) + 1;

        if ((value_length == 1) || FOURTH_FIELD_SIZE == 0) {
            return PROTO_OVERFLOW;
        }

        if (value_length > FOURTH_FIELD_SIZE) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->_fourth_field, 0, FOURTH_FIELD_SIZE);
        memcpy(this->_fourth_field, value, value_length);

        return PROTO_NO_ERROR;
    }

    int8_t UpdateFourthField(const char* value, uint16_t string_size) {
        if (value == nullptr) {
            return PROTO_INVAL_PTR;
        }

        if (FOURTH_FIELD_SIZE == 0) {
            return PROTO_OVERFLOW;
        }

        if (string_size > FOURTH_FIELD_SIZE) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->_fourth_field, 0, FOURTH_FIELD_SIZE);
        memcpy(this->_fourth_field, value, string_size);

        return PROTO_NO_ERROR;
    }

    int8_t UpdateFiveField(int64_t value) {
        this->_five_field = value;
        return PROTO_NO_ERROR;
    }

    int16_t Serialize(char* out_buffer, uint16_t out_buffer_size) const {
        if (out_buffer == nullptr) {
            return 0;
        }

        uint16_t serialized_size = sizeof(this->_first_field) + sizeof(this->_second_field) + sizeof(this->_third_field) + strlen(this->_fourth_field) + sizeof(this->_five_field);

        if (out_buffer_size < serialized_size) {
            return 0;
        }

        uint16_t offset = 0;

        memcpy(&out_buffer[offset], &this->_first_field, sizeof(this->_first_field));
        offset += sizeof(this->_first_field);
        memcpy(&out_buffer[offset], &this->_second_field, sizeof(this->_second_field));
        offset += sizeof(this->_second_field);
        memcpy(&out_buffer[offset], &this->_third_field, sizeof(this->_third_field));
        offset += sizeof(this->_third_field);
        memcpy(&out_buffer[offset], this->_fourth_field, strlen(this->_fourth_field) + 1);
        offset += strlen(this->_fourth_field) + 1;
        memcpy(&out_buffer[offset], &this->_five_field, sizeof(this->_five_field));

        return serialized_size;
    }

    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {
        if (in_buffer == nullptr) {
            return -1;
        }

        uint16_t deserialized_min_size = sizeof(this->_first_field) + sizeof(this->_second_field) + sizeof(this->_third_field) + sizeof(this->_five_field) + 1;

        if (in_buffer_size < deserialized_min_size) {
            return -3;
        }
        memset(this->_fourth_field, 0, FOURTH_FIELD_SIZE);

        uint16_t offset = 0;
        memcpy(&this->_first_field, &in_buffer[offset], sizeof(this->_first_field));
        offset += sizeof(this->_first_field);
        memcpy(&this->_second_field, &in_buffer[offset], sizeof(this->_second_field));
        offset += sizeof(this->_second_field);
        memcpy(&this->_third_field, &in_buffer[offset], sizeof(this->_third_field));
        offset += sizeof(this->_third_field);
        memcpy(this->_fourth_field, &in_buffer[offset], strlen(&in_buffer[offset]) + 1);
        offset += strlen(&in_buffer[offset]) + 1;
        memcpy(&this->_five_field, &in_buffer[offset], sizeof(this->_five_field));

        return 0;
    }

    int32_t SerializeJson(char* out_buffer, uint16_t out_buffer_size) {
        uint32_t response_length = 0;

        do {
            if (out_buffer == nullptr) {
                break;
            }

            StaticJsonDocument<512> doc;         
            doc["first_field"] = this->_first_field;         
            doc["second_field"] = this->_second_field;         
            doc["third_field"] = this->_third_field;         
            doc["fourth_field"] = this->_fourth_field;         
            doc["five_field"] = this->_five_field;
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
            if (!doc.containsKey("first_field")) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }
            if (!doc.containsKey("second_field")) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }
            if (!doc.containsKey("third_field")) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }
            if (!doc.containsKey("fourth_field")) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }
            if (!doc.containsKey("five_field")) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }
            if (this->UpdateFirstField(doc["first_field"])) {
                result = PROTO_INVAL_JSON_VALUE;
                break;
            }
            if (this->UpdateSecondField(doc["second_field"])) {
                result = PROTO_INVAL_JSON_VALUE;
                break;
            }
            if (this->UpdateThirdField(doc["third_field"])) {
                result = PROTO_INVAL_JSON_VALUE;
                break;
            }
            if (this->UpdateFourthField(doc["fourth_field"])) {
                result = PROTO_INVAL_JSON_VALUE;
                break;
            }
            if (this->UpdateFiveField(doc["five_field"])) {
                result = PROTO_INVAL_JSON_VALUE;
                break;
            }

            result = PROTO_NO_ERROR;

        } while(0);

        return result;
    }

private:
    uint8_t _first_field = 0;
    uint32_t _second_field = 0;
    uint16_t _third_field = 0;
    char _fourth_field[128] = {0};
    int64_t _five_field = 0;
};
#endif /* _TEST_PROTO_H */
