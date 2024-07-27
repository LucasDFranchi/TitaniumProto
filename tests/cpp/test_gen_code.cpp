#include "unity.h"
#include "TestProto.h"

void setUp(void)
{
    // Set up initial state before each test.
}

void tearDown(void)
{
    // Clean up after each test.
}

void test_UpdateFirstField(void)
{
    TestProtobuf protobuf{};
    uint8_t first_field = 0x10;

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateFirstField(first_field));
    TEST_ASSERT_EQUAL_UINT8(first_field, protobuf.GetFirstField());
}

void test_UpdateSecondField(void)
{
    TestProtobuf protobuf{};
    uint32_t second_field = 0xDEADBEEF;

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateSecondField(second_field));
    TEST_ASSERT_EQUAL_UINT32(second_field, protobuf.GetSecondField());
}

void test_UpdateThirdField(void)
{
    TestProtobuf protobuf{};
    uint16_t third_field = 0xDEAD;

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateThirdField(third_field));
    TEST_ASSERT_EQUAL_UINT16(third_field, protobuf.GetThirdField());
}

void test_UpdateFourthField(void)
{
    TestProtobuf protobuf{};
    const char *fourth_field = "Lucas";

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateFourthField(fourth_field));
    TEST_ASSERT_EQUAL_STRING(fourth_field, protobuf.GetFourthField());
}

void test_UpdateFourthFieldNullBuffer(void)
{
    TestProtobuf protobuf{};
    const char *fourth_field = nullptr;

    TEST_ASSERT_EQUAL_INT8(PROTO_INVAL_PTR, protobuf.UpdateFourthField(fourth_field));
    TEST_ASSERT_EQUAL_STRING("", protobuf.GetFourthField());
}

void test_UpdateFourthFieldZeroLengthString(void)
{
    TestProtobuf protobuf{};
    const char *fourth_field = "";

    TEST_ASSERT_EQUAL_INT8(PROTO_OVERFLOW, protobuf.UpdateFourthField(fourth_field));
    TEST_ASSERT_EQUAL_STRING("", protobuf.GetFourthField());
}

void test_UpdateFourthFieldMissingNullTerminator(void)
{
    TestProtobuf protobuf{};
    const char *fourth_field = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut e";

    TEST_ASSERT_EQUAL_INT8(PROTO_INVAL_SIZE, protobuf.UpdateFourthField(fourth_field));
    TEST_ASSERT_EQUAL_STRING("", protobuf.GetFourthField());
}

void test_UpdateFourthFieldMissingNullTerminatorFixedSize(void)
{
    TestProtobuf protobuf{};
    const char *fourth_field = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.";

    TEST_ASSERT_EQUAL_INT8(PROTO_INVAL_SIZE, protobuf.UpdateFourthField(fourth_field, strlen(fourth_field)));
    TEST_ASSERT_EQUAL_STRING("", protobuf.GetFourthField());
}

void test_UpdateFiveField(void)
{
    TestProtobuf protobuf{};
    int64_t five_field = 0xDEADBEEFBADC0FFE;

    TEST_ASSERT_EQUAL_INT8(0, protobuf.UpdateFiveField(five_field));
    TEST_ASSERT_EQUAL_INT64(five_field, protobuf.GetFiveField());
}

void test_Serialize(void)
{
    TestProtobuf protobuf;
    char buffer[512]; // Adjust size as necessary

    // Set values
    protobuf.UpdateFirstField(0x0A);
    protobuf.UpdateSecondField(0xDEADBEEF);
    protobuf.UpdateThirdField(0xBAAD);
    protobuf.UpdateFourthField("This is not a very long string");
    protobuf.UpdateFiveField(0xDEADBEEFBADC0FFE);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    // Check if serialization succeeded
    TEST_ASSERT_GREATER_THAN_INT16(0, serialized_size);
}

void test_Deserialize(void)
{
    TestProtobuf protobuf{};
    char buffer[512]; // Adjust size as necessary

    uint8_t expected_first_data = 0x0A;
    uint32_t expected_second_data = 0xDEADBEEF;
    uint16_t expected_third_data = 0xBAAD;
    const char *expected_fourth_data = "This is not a very long string";
    int64_t expected_five_data = 0xFFADBEEFBADC0FFE;

    // Set values
    protobuf.UpdateFirstField(expected_first_data);
    protobuf.UpdateSecondField(expected_second_data);
    protobuf.UpdateThirdField(expected_third_data);
    protobuf.UpdateFourthField(expected_fourth_data);
    protobuf.UpdateFiveField(expected_five_data);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    TestProtobuf protobuf_new{};

    // Perform deserialization
    TEST_ASSERT_EQUAL_INT8(0, protobuf_new.DeSerialize(buffer, serialized_size));

    // Check if deserialization populated values correctly
    TEST_ASSERT_EQUAL_UINT8(expected_first_data, protobuf_new.GetFirstField());
    TEST_ASSERT_EQUAL_UINT32(expected_second_data, protobuf_new.GetSecondField());
    TEST_ASSERT_EQUAL_UINT16(expected_third_data, protobuf_new.GetThirdField());
    TEST_ASSERT_EQUAL_STRING(expected_fourth_data, protobuf_new.GetFourthField());
    TEST_ASSERT_EQUAL_INT64(expected_five_data, protobuf_new.GetFiveField());
}

void test_SerializeInputBufferNull(void)
{
    TestProtobuf protobuf;
    char *buffer = nullptr; // Adjust size as necessary

    // Set values
    protobuf.UpdateFirstField(0x0A);
    protobuf.UpdateSecondField(0xDEADBEEF);
    protobuf.UpdateThirdField(0xBAAD);
    protobuf.UpdateFourthField("This is not a very long string");
    protobuf.UpdateFiveField(0xDEADBEEFBADC0FFE);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    // Check if serialization succeeded
    TEST_ASSERT_EQUAL_UINT8(0, serialized_size);
}

void test_SerializeInputBufferOverflow(void)
{
    TestProtobuf protobuf;
    char buffer[32]; // Adjust size as necessary

    // Set values
    protobuf.UpdateFirstField(0x0A);
    protobuf.UpdateSecondField(0xDEADBEEF);
    protobuf.UpdateThirdField(0xBAAD);
    protobuf.UpdateFourthField("This is not a very long string");
    protobuf.UpdateFiveField(0xDEADBEEFBADC0FFE);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    // Check if serialization succeeded
    TEST_ASSERT_EQUAL_UINT8(0, serialized_size);
}

void test_DeserializeOutputBufferUnderflow(void)
{
    TestProtobuf protobuf{};
    char buffer[512]; // Adjust size as necessary

    uint8_t expected_first_data = 0x0A;
    uint32_t expected_second_data = 0xDEADBEEF;
    uint16_t expected_third_data = 0xBAAD;
    const char *expected_fourth_data = "This is not a very long string";
    int64_t expected_five_data = 0xFFADBEEFBADC0FFE;

    // Set values
    protobuf.UpdateFirstField(expected_first_data);
    protobuf.UpdateSecondField(expected_second_data);
    protobuf.UpdateThirdField(expected_third_data);
    protobuf.UpdateFourthField(expected_fourth_data);
    protobuf.UpdateFiveField(expected_five_data);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    TestProtobuf protobuf_new{};
    char buffer_deserilize[12]; // Adjust size as necessary

    // Perform deserialization
    TEST_ASSERT_EQUAL_INT8(PROTO_INVAL_SIZE, protobuf_new.DeSerialize(buffer_deserilize, sizeof(buffer_deserilize)));
}

void test_DeserializeOutputBufferNull(void)
{
    TestProtobuf protobuf{};
    char buffer[512]; // Adjust size as necessary

    uint8_t expected_first_data = 0x0A;
    uint32_t expected_second_data = 0xDEADBEEF;
    uint16_t expected_third_data = 0xBAAD;
    const char *expected_fourth_data = "This is not a very long string";
    int64_t expected_five_data = 0xFFADBEEFBADC0FFE;

    // Set values
    protobuf.UpdateFirstField(expected_first_data);
    protobuf.UpdateSecondField(expected_second_data);
    protobuf.UpdateThirdField(expected_third_data);
    protobuf.UpdateFourthField(expected_fourth_data);
    protobuf.UpdateFiveField(expected_five_data);

    // Perform serialization
    int16_t serialized_size = protobuf.Serialize(buffer, sizeof(buffer));

    TestProtobuf protobuf_new{};
    const char* buffer_deserilize = nullptr; // Adjust size as necessary

    // Perform deserialization
    TEST_ASSERT_EQUAL_INT8(PROTO_INVAL_PTR, protobuf_new.DeSerialize(buffer_deserilize, sizeof(buffer_deserilize)));
}

void test_SerializeJson(void)
{
    TestProtobuf protobuf;
    char buffer[512]; // Adjust size as necessary

    const char *expected_json = "{\"first_field\":254,\"second_field\":3131817711,\"third_field\":47789,\"fourth_field\":\"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut\",\"five_field\":-1146443043}";

    // Set values
    protobuf.UpdateFirstField(254);
    protobuf.UpdateSecondField(3131817711);
    protobuf.UpdateThirdField(47789);
    protobuf.UpdateFourthField("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut");
    protobuf.UpdateFiveField(-1146443043);

    auto deserializeResult = protobuf.SerializeJson(buffer, sizeof(buffer));
    TEST_ASSERT_GREATER_THAN_INT16(0, deserializeResult);
    TEST_ASSERT_EQUAL_STRING(expected_json, buffer);
}

void test_SerializeJsonOutputBufferNull(void)
{
    TestProtobuf protobuf;
    char *buffer = nullptr; // Adjust size as necessary

    const char *expected_json = "{\n    \"first_field\":254,\n    \"second_field\":3131817711,\n    \"third_field\":47789,\n    \"fourth_field\":\"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut\",\n    \"five_field\":-1146443043\n}";

    // Set values
    protobuf.UpdateFirstField(254);
    protobuf.UpdateSecondField(3131817711);
    protobuf.UpdateThirdField(47789);
    protobuf.UpdateFourthField("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut");
    protobuf.UpdateFiveField(-1146443043);

    auto deserializeResult = protobuf.SerializeJson(buffer, sizeof(buffer));
    TEST_ASSERT_EQUAL_INT8(0, deserializeResult);
}

void test_DeSerializeJson(void)
{
    TestProtobuf protobuf;
    char buffer[512]; // Adjust size as necessary

    uint8_t expected_first_data = 0x0A;
    uint32_t expected_second_data = 0xDEADBEEF;
    uint16_t expected_third_data = 0xBAAD;
    const char *expected_fourth_data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut";
    int64_t expected_five_data = -5764607523034234881;

    // Serialize data into buffer
    protobuf.UpdateFirstField(expected_first_data);
    protobuf.UpdateSecondField(expected_second_data);
    protobuf.UpdateThirdField(expected_third_data);
    protobuf.UpdateFourthField(expected_fourth_data);
    protobuf.UpdateFiveField(expected_five_data);
    int16_t serialized_size = protobuf.SerializeJson(buffer, sizeof(buffer));
    TEST_ASSERT_GREATER_THAN_INT16(0, serialized_size);

    // Clear existing data in protobuf instance
    TestProtobuf protobuf_new{};

    // Perform deserialization
    TEST_ASSERT_EQUAL_INT8(0, protobuf_new.DeSerializeJson(buffer, sizeof(buffer)));

    // Check if deserialization populated values correctly
    TEST_ASSERT_EQUAL_UINT8(expected_first_data, protobuf_new.GetFirstField());
    TEST_ASSERT_EQUAL_UINT32(expected_second_data, protobuf_new.GetSecondField());
    TEST_ASSERT_EQUAL_UINT16(expected_third_data, protobuf_new.GetThirdField());
    TEST_ASSERT_EQUAL_STRING(expected_fourth_data, protobuf_new.GetFourthField());
    TEST_ASSERT_EQUAL_INT64(expected_five_data, protobuf_new.GetFiveField());
}

int main(void)
{
    UNITY_BEGIN();

    // Run tests
    RUN_TEST(test_UpdateFirstField);
    RUN_TEST(test_UpdateSecondField);
    RUN_TEST(test_UpdateThirdField);
    RUN_TEST(test_UpdateFourthField);
    RUN_TEST(test_UpdateFourthFieldNullBuffer);
    RUN_TEST(test_UpdateFourthFieldZeroLengthString);
    RUN_TEST(test_UpdateFourthFieldMissingNullTerminator);
    RUN_TEST(test_UpdateFourthFieldMissingNullTerminatorFixedSize);
    RUN_TEST(test_UpdateFiveField);
    RUN_TEST(test_Serialize);
    RUN_TEST(test_Deserialize);
    RUN_TEST(test_SerializeInputBufferOverflow);
    RUN_TEST(test_SerializeInputBufferNull);
    RUN_TEST(test_DeserializeOutputBufferUnderflow);
    RUN_TEST(test_DeserializeOutputBufferNull);
    RUN_TEST(test_SerializeJson);
    RUN_TEST(test_DeSerializeJson);

    UNITY_END();

    return 0;
}
