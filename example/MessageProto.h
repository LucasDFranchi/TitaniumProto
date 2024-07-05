#ifndef MESSAGE_PROTO_H
#define MESSAGE_PROTO_H

#include "stdint.h"
#include "string.h"

class MessageProtobuf {
public:
    MessageProtobuf() = default;
    ~MessageProtobuf() = default;

    static constexpr uint16_t BUFFER_SIZE = 32;
    static constexpr uint16_t BUFFER_2_SIZE = 128;

    int64_t GetTimestamp(void) const {  return this->_timestamp; }
    const char* GetBuffer(void) const {  return this->_buffer; }
    const char* GetBuffer2(void) const {  return this->_buffer_2; }
    int32_t GetId(void) const {  return this->_id; }

    int16_t GetSerializedSize(void) const {
        return (sizeof(this->_timestamp) + (strlen(this->_buffer) + 1) + (strlen(this->_buffer_2) + 1) + sizeof(this->_id));
    }

    int16_t GetMaxSize(void) const {
        return (sizeof(this->_timestamp) + sizeof(this->_buffer) + sizeof(this->_buffer_2) + sizeof(this->_id));
    }

    static int16_t GetStaticMaxSize(void) {
        return (sizeof(int64_t) + BUFFER_SIZE + BUFFER_2_SIZE + sizeof(int32_t));
    }

    int8_t UpdateTimestamp(int64_t value) {
        this->_timestamp = value;
        return 0;
    }

    int8_t UpdateBuffer(char* value) {
        if (value == nullptr) {
            return -1;
        }

        size_t value_length = strlen(value) + 1;

        if ((value_length == 0) || BUFFER_SIZE == 0) {
            return -2;
        }

        if (value_length > BUFFER_SIZE) {
            return -3;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);
        memcpy(this->_buffer, value, value_length);

        return 0;
    }

    int8_t UpdateBuffer2(char* value) {
        if (value == nullptr) {
            return -1;
        }

        size_t value_length = strlen(value) + 1;

        if ((value_length == 0) || BUFFER_2_SIZE == 0) {
            return -2;
        }

        if (value_length > BUFFER_2_SIZE) {
            return -3;
        }

        memset(this->_buffer_2, 0, BUFFER_2_SIZE);
        memcpy(this->_buffer_2, value, value_length);

        return 0;
    }

    int8_t UpdateId(int32_t value) {
        this->_id = value;
        return 0;
    }

    int16_t Serialize(char* out_buffer, uint16_t out_buffer_size) const {
        if (out_buffer == nullptr) {
            return 0;
        }

        uint16_t serialized_size = sizeof(this->_timestamp) + (strlen(this->_buffer) + 1) + (strlen(this->_buffer_2) + 1) + sizeof(this->_id);

        if (out_buffer_size < serialized_size) {
            return 0;
        }

        uint16_t offset = 0;

        memcpy(&out_buffer[offset], &this->_timestamp, sizeof(this->_timestamp));
        offset += sizeof(this->_timestamp);
        memcpy(&out_buffer[offset], this->_buffer, strlen(this->_buffer) + 1);
        offset += strlen(this->_buffer) + 1;
        memcpy(&out_buffer[offset], this->_buffer_2, strlen(this->_buffer_2) + 1);
        offset += strlen(this->_buffer_2) + 1;
        memcpy(&out_buffer[offset], &this->_id, sizeof(this->_id));
    
        return serialized_size;
    }

    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {
        if (in_buffer == nullptr) {
            return -1;
        }

        uint16_t deserialized_min_size = sizeof(this->_timestamp) + sizeof(this->_id) + 2;
        uint16_t deserialized_max_size = sizeof(this->_timestamp) + sizeof(this->_buffer) + sizeof(this->_buffer_2) + sizeof(this->_id);

        if (in_buffer_size < deserialized_min_size) {
            return -3;
        }

        if (in_buffer_size > deserialized_max_size) {
            return -3;
        }

        memset(this->_buffer, 0, BUFFER_SIZE);
        memset(this->_buffer_2, 0, BUFFER_2_SIZE);

        uint16_t offset = 0;
        memcpy(&this->_timestamp, &in_buffer[offset], sizeof(this->_timestamp));
        offset += sizeof(this->_timestamp);
        memcpy(this->_buffer, &in_buffer[offset], strlen(&in_buffer[offset]) + 1);
        offset += strlen(&in_buffer[offset]) + 1;
        memcpy(this->_buffer_2, &in_buffer[offset], strlen(&in_buffer[offset]) + 1);
        offset += strlen(&in_buffer[offset]) + 1;
        memcpy(&this->_id, &in_buffer[offset], sizeof(this->_id));
    
        return 0;
    }

private:
    int64_t _timestamp = 0;
    char _buffer[32] = {0};
    char _buffer_2[128] = {0};
    int32_t _id = 0;
};

#endif /* MESSAGE_PROTO_H */ 

