/**
 * @file TestProtobuf.h
 * @brief Auto-generated header file generated.
 */

#ifndef TEST_PROTO_H
#define TEST_PROTO_H

#include "stdint.h"
#include "string.h"
#include "jsmn.h"

#ifndef PROTOBUFS_ERRORS_H
#define PROTOBUFS_ERRORS_H

enum protobufs_errors {
  PROTO_NO_ERROR   = 0,
  PROTO_INVAL_PTR  = -1,
  PROTO_OVERFLOW   = -2,
  PROTO_INVAL_SIZE = -3,
  PROTO_INVAL_NUM_TOKEN = -4,
  PROTO_INVAL_JSON_KEY = -5,
};

#endif // PROTOBUFS_ERRORS_H

class TestProtobuf {
public:
    TestProtobuf() = default;
    ~TestProtobuf() = default;

    static constexpr uint16_t BUFFER_SIZE = 128;

    uint64_t GetTimestamp(void) const { return this->_timestamp; }
    const char* GetBuffer(void) const { return this->_buffer; }
    int32_t GetId(void) const { return this->_id; }

    int16_t GetSerializedSize(void) const {
        return (sizeof(this->_timestamp) + (strlen(this->_buffer) + 1) + sizeof(this->_id));
    }

    int16_t GetMaxSize(void) const {
        return (sizeof(this->_timestamp) + sizeof(this->_buffer) + sizeof(this->_id));
    }

    static int16_t GetStaticMaxSize(void) {
        return (sizeof(uint64_t) + BUFFER_SIZE + sizeof(int32_t));
    }

    int8_t UpdateTimestamp(uint64_t value) {
        this->_timestamp = value;
        return PROTO_NO_ERROR;
    }

    int8_t UpdateBuffer(const char* value) {
        if (value == nullptr) {
            return PROTO_INVAL_PTR;
        }

        size_t value_length = strlen(value) + 1;

        if ((value_length == 0) || BUFFER_SIZE == 0) {
            return PROTO_OVERFLOW;
        }

        if (value_length > BUFFER_SIZE) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);
        memcpy(this->_buffer, value, value_length);

        return PROTO_NO_ERROR;
    }

    int8_t UpdateBuffer(const char* value, uint16_t string_size) {
        if (value == nullptr) {
            return PROTO_INVAL_PTR;
        }

        if (BUFFER_SIZE == 0) {
            return PROTO_OVERFLOW;
        }

        if (string_size > BUFFER_SIZE) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);
        memcpy(this->_buffer, value, string_size);

        return PROTO_NO_ERROR;
    }

    int8_t UpdateId(int32_t value) {
        this->_id = value;
        return PROTO_NO_ERROR;
    }

    int16_t Serialize(char* out_buffer, uint16_t out_buffer_size) const {
        if (out_buffer == nullptr) {
            return 0;
        }

        uint16_t serialized_size = sizeof(this->_timestamp) + (strlen(this->_buffer) + 1) + sizeof(this->_id);

        if (out_buffer_size < serialized_size) {
            return 0;
        }

        uint16_t offset = 0;

        memcpy(&out_buffer[offset], &this->_timestamp, sizeof(this->_timestamp));
        offset += sizeof(this->_timestamp);
        memcpy(&out_buffer[offset], this->_buffer, strlen(this->_buffer) + 1);
        offset += strlen(this->_buffer) + 1;
        memcpy(&out_buffer[offset], &this->_id, sizeof(this->_id));

        return serialized_size;
    }

    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {
        if (in_buffer == nullptr) {
            return PROTO_INVAL_PTR;
        }

        uint16_t deserialized_min_size = sizeof(this->_timestamp) + sizeof(this->_id) + 1;
        uint16_t deserialized_max_size = sizeof(this->_timestamp) + sizeof(this->_buffer) + sizeof(this->_id);

        if ((in_buffer_size < deserialized_min_size) || (in_buffer_size > deserialized_max_size)) {
            return PROTO_INVAL_SIZE;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);

        uint16_t offset = 0;
        memcpy(&this->_timestamp, &in_buffer[offset], sizeof(this->_timestamp));
        offset += sizeof(this->_timestamp);
        memcpy(this->_buffer, &in_buffer[offset], strlen(&in_buffer[offset]) + 1);
        offset += strlen(&in_buffer[offset]) + 1;
        memcpy(&this->_id, &in_buffer[offset], sizeof(this->_id));

        return PROTO_NO_ERROR;
    }
    int32_t SerializeJson(char* out_buffer, uint16_t out_buffer_size) {
        uint32_t response_length = 0;

        do {
            if (out_buffer == nullptr) {
                break;
            }

            uint16_t serialized_size = sizeof(this->_timestamp) + (strlen(this->_buffer) + 1) + sizeof(this->_id);

            if (out_buffer_size < serialized_size) {
                return 0;
            }

            response_length = snprintf(out_buffer, out_buffer_size,
                                       this->_json_string,
                                       this->_timestamp,
                                       this->_buffer,
                                       this->_id);
        } while (0);

        return response_length;
    }

    int8_t DeSerializeJson(const char* in_buffer, uint16_t in_buffer_size) {
        auto result = PROTO_NO_ERROR;
        jsmn_parser parser;
        jsmntok_t tokens[this->_NUM_TOKENS];

        jsmn_init(&parser);

        do {
            if (in_buffer == nullptr) {
                result = PROTO_INVAL_PTR;
                break;
            }

            auto num_tokens = jsmn_parse(&parser, in_buffer, strlen(in_buffer), tokens, this->_NUM_TOKENS);

            if (num_tokens != this->_NUM_TOKENS) {
                result = PROTO_INVAL_NUM_TOKEN;
                break;
            }

            jsmntok_t key{};
            jsmntok_t value{};
            uint16_t token_length = 0;

            key   = tokens[this->_TIMESTAMP_TOKEN_ID];
            value = tokens[this->_TIMESTAMP_TOKEN_ID + 1];
            token_length = key.end - key.start;

            if (strncmp(in_buffer + key.start, this->_TIMESTAMP_TOKEN_NAME, token_length) != 0) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }

            this->UpdateTimestamp(atoi(in_buffer + value.start));

            key   = tokens[this->_BUFFER_TOKEN_ID];
            value = tokens[this->_BUFFER_TOKEN_ID + 1];
            token_length = key.end - key.start;

            if (strncmp(in_buffer + key.start, this->_BUFFER_TOKEN_NAME, token_length) != 0) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }

            this->UpdateBuffer(in_buffer + value.start, value.end - value.start);

            key   = tokens[this->_ID_TOKEN_ID];
            value = tokens[this->_ID_TOKEN_ID + 1];
            token_length = key.end - key.start;

            if (strncmp(in_buffer + key.start, this->_ID_TOKEN_NAME, token_length) != 0) {
                result = PROTO_INVAL_JSON_KEY;
                break;
            }

            this->UpdateId(atoi(in_buffer + value.start));

            result = PROTO_NO_ERROR;

        } while(0);

        return result;
    }

private:
    uint64_t _timestamp = 0;
    char _buffer[128] = {0};
    int32_t _id = 0;
    const char* _json_string = R"({
    "timestamp": %llu,
    "buffer": "%s",
    "id": %d
})";  
    const char* _TIMESTAMP_TOKEN_NAME = "timestamp";
    const uint8_t _TIMESTAMP_TOKEN_ID = 1;  
    const char* _BUFFER_TOKEN_NAME = "buffer";
    const uint8_t _BUFFER_TOKEN_ID = 3;  
    const char* _ID_TOKEN_NAME = "id";
    const uint8_t _ID_TOKEN_ID = 5;
    const uint8_t _NUM_TOKENS  = 7;
};
#endif /* TEST_PROTO_H */
