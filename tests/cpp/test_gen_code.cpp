#include "unity.h"
#include "TestProto.h"

void setUp(void) {
    // Set up initial state before each test.
}

void tearDown(void) {
    // Clean up after each test.
}

void test_UpdateTimestamp(void) {
    TestProtobuf protobuf;
    uint64_t timestamp = 1234567890;

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateTimestamp(timestamp));
    TEST_ASSERT_EQUAL_UINT64(timestamp, protobuf.GetTimestamp());
}

void test_UpdateBuffer(void) {
    TestProtobuf protobuf;
    const char* buffer = "Hello, World!";

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateBuffer(buffer));
    TEST_ASSERT_EQUAL_STRING(buffer, protobuf.GetBuffer());
}

void test_UpdateId(void) {
    TestProtobuf protobuf;
    int32_t id = 987;

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateId(id));
    TEST_ASSERT_EQUAL_INT32(id, protobuf.GetId());
}

void test_Serialize(void) {
    TestProtobuf protobuf;
    char buffer[512];  // Adjust size as necessary

    // Set values
    protobuf.UpdateTimestamp(1234567890);
    protobuf.UpdateBuffer("Hello, World!");
    protobuf.UpdateId(987);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    // Check if serialization succeeded
    TEST_ASSERT_GREATER_THAN_INT16(0, serialized_size);
}

void test_SerializeJson(void) {
    TestProtobuf protobuf;
    char buffer[512];  // Adjust size as necessary

    const char* expected_json = "{\n    \"timestamp\": 1234567890,\n    \"buffer\": \"Hello, World!\",\n    \"id\": 987\n}";

    // Set values
    protobuf.UpdateTimestamp(1234567890);
    protobuf.UpdateBuffer("Hello, World!");
    protobuf.UpdateId(987);

    auto deserializeResult = protobuf.SerializeJson(buffer, sizeof(buffer));
    TEST_ASSERT_GREATER_THAN_INT16(0, deserializeResult);
    TEST_ASSERT_EQUAL_STRING(expected_json, buffer);
}

void test_Deserialize(void) {
    TestProtobuf protobuf;
    char buffer[512];  // Adjust size as necessary

    // Serialize data into buffer
    protobuf.UpdateTimestamp(1234567890);
    protobuf.UpdateBuffer("Hello, World!");
    protobuf.UpdateId(987);
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    // Clear existing data in protobuf instance
    protobuf.UpdateTimestamp(0);
    protobuf.UpdateBuffer("");
    protobuf.UpdateId(0);

    // Perform deserialization
    TEST_ASSERT_EQUAL_INT8(0, protobuf.DeSerialize(buffer, serialized_size));

    // Check if deserialization populated values correctly
    TEST_ASSERT_EQUAL_UINT64(1234567890, protobuf.GetTimestamp());
    TEST_ASSERT_EQUAL_STRING("Hello, World!", protobuf.GetBuffer());
    TEST_ASSERT_EQUAL_INT32(987, protobuf.GetId());
}

void test_DeSerializeJson(void) {
    TestProtobuf protobuf;
    char buffer[512];  // Adjust size as necessary

    // Serialize data into buffer
    protobuf.UpdateTimestamp(1234567890);
    protobuf.UpdateBuffer("Hello World!");
    protobuf.UpdateId(987);
    int16_t serialized_size = protobuf.SerializeJson(buffer, sizeof(buffer));

    // Clear existing data in protobuf instance
    protobuf.UpdateTimestamp(0);
    protobuf.UpdateBuffer("");
    protobuf.UpdateId(0);

    // Perform deserialization
    TEST_ASSERT_EQUAL_INT8(0, protobuf.DeSerializeJson(buffer, sizeof(buffer)));


    // Check if deserialization populated values correctly
    TEST_ASSERT_EQUAL_UINT64(1234567890, protobuf.GetTimestamp());
    TEST_ASSERT_EQUAL_STRING("Hello World!", protobuf.GetBuffer());
    TEST_ASSERT_EQUAL_INT32(987, protobuf.GetId());
}

// Define more test cases as needed

int main(void) {
    UNITY_BEGIN();

    // Run tests
    RUN_TEST(test_UpdateTimestamp);
    RUN_TEST(test_UpdateBuffer);
    RUN_TEST(test_UpdateId);
    RUN_TEST(test_Serialize);
    RUN_TEST(test_SerializeJson);
    RUN_TEST(test_Deserialize);
    RUN_TEST(test_DeSerializeJson);

    // Add more RUN_TEST macros for additional tests

    UNITY_END();

    return 0;
}
