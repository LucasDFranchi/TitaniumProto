#include <stdlib.h>

class SafeConverter {
public:
    static int8_t to_uint8_t(const char *str, uint8_t &result) {
        return convert(str, result, sizeof(uint8_t));
    }

    static int8_t to_uint16_t(const char *str, uint16_t &result) {
        return convert(str, result, sizeof(uint16_t));
    }

    static int8_t to_uint32_t(const char *str, uint32_t &result) {
        return convert(str, result, sizeof(uint32_t));
    }

    static int8_t to_uint64_t(const char *str, uint64_t &result) {
        return convert(str, result, sizeof(uint64_t));
    }

    static int8_t to_int8_t(const char *str, int8_t &result) {
        return convert(str, result, sizeof(int8_t));
    }

    static int8_t to_int16_t(const char *str, int16_t &result) {
        return convert(str, result, sizeof(int16_t));
    }

    static int8_t to_int32_t(const char *str, int32_t &result) {
        return convert(str, result, sizeof(int32_t));
    }

    static int8_t to_int64_t(const char *str, int64_t &result) {
        return convert(str, result, sizeof(int64_t));
    }

private:
    template <typename T>
    static int8_t convert(const char *str, T &result, uint8_t size) {
        char *endptr;
        

        unsigned long value = strtoul(str, &endptr, 10);

        if (*endptr != '\0' || endptr == str) {
            return -1; // Invalid input
        }
    
        result = static_cast<T>(value);
        return 0;
    }
};