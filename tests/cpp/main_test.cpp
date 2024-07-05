#include <iostream>
#include "TestProto.h"

int main() {
    // Create an instance of TestProtobuf
    TestProtobuf testObj;

    // Update values
    testObj.UpdateTimestamp(1234567890);
    testObj.UpdateBuffer("Hello, protobuf!");
    testObj.UpdateId(987);

    // Serialize to a buffer
    char serializedBuffer[TestProtobuf::BUFFER_SIZE];
    uint16_t serializedSize = testObj.Serialize(serializedBuffer, TestProtobuf::BUFFER_SIZE);

    if (serializedSize > 0) {
        std::cout << "Serialization successful. Serialized size: " << serializedSize << std::endl;

        // Print serialized data (for demonstration)
        std::cout << "Serialized data: ";
        for (int i = 0; i < serializedSize; ++i) {
            printf("%x ", serializedBuffer[i]);
        }
        std::cout << std::endl;

        // Create a new instance to deserialize into
        TestProtobuf deserializedObj;

        // Deserialize
        int8_t deserializeResult = deserializedObj.DeSerialize(serializedBuffer, serializedSize);

        if (deserializeResult == 0) {
            std::cout << "Deserialization successful." << std::endl;

            // Get and print deserialized values
            std::cout << "Deserialized timestamp: " << deserializedObj.GetTimestamp() << std::endl;
            std::cout << "Deserialized buffer: " << deserializedObj.GetBuffer() << std::endl;
            std::cout << "Deserialized id: " << deserializedObj.GetId() << std::endl;
        } else {
            std::cerr << "Deserialization failed with error code: " << static_cast<int>(deserializeResult) << std::endl;
        }

        char buffer[1024] = {0};
        deserializeResult = deserializedObj.SerializeJson(buffer, sizeof(buffer));

        if (deserializeResult > 0) {
            std::cout << buffer << std::endl;        
        } else {
            std::cerr << "Deserialization failed with error code: " << static_cast<int>(deserializeResult) << std::endl;
        }

        // Create a new instance to deserialize into
        TestProtobuf deserializedJsonObj;

        // Deserialize
        int8_t deserializeJsonResult = deserializedJsonObj.DeSerializeJson(buffer, sizeof(buffer));

        if (deserializeJsonResult == 0) {
            std::cout << "Deserialization successful." << std::endl;

            // Get and print deserialized values
            std::cout << "Deserialized timestamp: " << deserializedJsonObj.GetTimestamp() << std::endl;
            std::cout << "Deserialized buffer: " << deserializedJsonObj.GetBuffer() << std::endl;
            std::cout << "Deserialized id: " << deserializedJsonObj.GetId() << std::endl;
        } else {
            std::cerr << "Deserialization failed with error code: " << static_cast<int>(deserializeJsonResult) << std::endl;
        }

    } else {
        std::cerr << "Serialization failed." << std::endl;
    }


    return 0;
}
