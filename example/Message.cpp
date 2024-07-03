#include "stdint.h"
#include "string.h"

namespace Errors {
    constexpr int8_t NO_ERROR = 0;
    constexpr int8_t INVALID_BUFFER_PTR = -1;
    constexpr int8_t INVALID_BUFFER_SIZE = -2;
    constexpr int8_t OVERFLOW_BUFFER = -3;
}

class MessageProtobuf {
public:
    MessageProtobuf() = default;
    ~MessageProtobuf() = default;

    static constexpr uint16_t BUFFER_SIZE = 32;

    int64_t GetTimestamp(void) const {  return this->_timestamp; }
    const char* GetBuffer(void) const {  return this->_buffer; }
    int32_t GetId(void) const {  return this->_id; }

    int8_t UpdateTimestamp(int64_t value) {
        this->_timestamp = value;
        return Errors::NO_ERROR;
    }

    int8_t UpdateBuffer(char* value) {
        if (value == nullptr || this->_buffer == nullptr) {
            return Errors::INVALID_BUFFER_PTR;
        }

        size_t value_length = strlen(value) + 1;

        if ((value_length == 0) || BUFFER_SIZE == 0) {
            return Errors::INVALID_BUFFER_SIZE;
        }

        if (value_length > BUFFER_SIZE) {
            return Errors::OVERFLOW_BUFFER;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);
        memcpy(this->_buffer, value, value_length);

        return Errors::NO_ERROR;
    }

    int8_t UpdateId(int32_t value) {
        this->_id = value;
        return Errors::NO_ERROR;
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
            return Errors::INVALID_BUFFER_PTR;
        }

        uint16_t deserialized_min_size = sizeof(this->_timestamp) + 1 + sizeof(this->_id);
        uint16_t deserialized_max_size = sizeof(this->_timestamp) + sizeof(this->_buffer) + sizeof(this->_id);

        if (in_buffer_size < deserialized_min_size) {
            return Errors::OVERFLOW_BUFFER;
        }

        if (in_buffer_size > deserialized_max_size) {
            return Errors::OVERFLOW_BUFFER;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);

        uint16_t offset = 0;
        memcpy(&this->_timestamp, &in_buffer[offset], sizeof(this->_timestamp));
        offset += sizeof(this->_timestamp);
        memcpy(this->_buffer, &in_buffer[offset], strlen(&in_buffer[offset]) + 1);
        offset += strlen(&in_buffer[offset]) + 1;
        memcpy(&this->_id, &in_buffer[offset], sizeof(this->_id));
    
        return Errors::NO_ERROR;
    }

private:
    int64_t _timestamp = 0;
    char _buffer[32] = {0};
    int32_t _id = 0;
};