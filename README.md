# TitaniumProto

TitaniumProto is a Python library designed to facilitate working with C++ structs. It reads a JSON file in a specific format and converts it into a C++ class that closely mirrors the JSON structure. The generated class includes methods for serializing and deserializing data, making it suitable for embedded systems and other applications requiring efficient data handling.

## Motivation

I created this project to streamline the process of defining and managing data structures in C++ projects. By using a JSON-based format, TitaniumProto enables quick prototyping and seamless integration of structured data into C++ applications. The generated C++ classes offer serialization and deserialization capabilities, ensuring data integrity and efficiency in memory-constrained environments.

## Features

- Converts JSON definitions into C++ class structures.
- Supports serialization and deserialization of data.
- Easy integration into existing C++ projects.
- Lightweight and suitable for embedded systems.

## Limitations

- The maximum string size is 256 bytes.
- The maximum Json size is 1024 bytes.
- The library doesn't support Json Arrays. [wip]
- The library doesn't support nested Json.

## Why Rely on ArduinoJson?

In the realm of C and C++ programming, there are several popular libraries for handling JSON, such as jsmn, cJSON, and nlohmann's JSON. However, each of these libraries has its limitations:

  -  jsmn: This library does not support JSON serialization, only parsing.
  -  cJSON and nlohmann's JSON: Both of these libraries rely on heap allocation for JSON serialization and parsing. This can pose challenges in embedded environments using operating systems like FreeRTOS, as they depend on functions like malloc, realloc, and free, which may not be fully compatible with FreeRTOS.

ArduinoJson version 6 addresses these issues by supporting JSON parsing and serialization using stack allocation. This approach avoids problems associated with custom allocators in FreeRTOS and mitigates issues like heap fragmentation and memory leaks. However, it's important to note that using stack allocation may lead to stack overflow with larger JSON files, so ArduinoJson is best suited for handling smaller JSON files.

## Installation

To install TitaniumProto, you can use pip or clone the repository and install dependencies:

Windows

```bash
pip install titanium-proto
```

Linux

```bash
pip3 install titanium-proto
```

Installation using clone and poetry:

```bash
git clone https://github.com/your_username/titanium-proto.git
cd titanium-proto
poetry install
```

### Usage

Define Your JSON Structure: Create a JSON file following the specified format.
Generate C++ Class: Use TitaniumProto to convert the JSON into a C++ class.
Integrate: Include the generated C++ class in your project and utilize its methods for data handling.


### Supported Types
The library supports the following data types, each with specific attributes:

- **uint8_t**
- **int8_t**
- **uint16_t**
- **int16_t**
- **uint32_t**
- **int32_t**
- **uint64_t**
- **int64_t**
- **float**
- **double**
- **string**: This type should have a `maximum_size` associated.

### Example

Consider a JSON file example.json:

``` json
{
  "package": "ExamplePackage",
  "syntax": "titanium1",
  "fields": [
    { "name": "id", "type": "uint32_t" },
    { "name": "name", "type": "string", "maximum_size": 32 },
    { "name": "value", "type": "double" }
  ]
}
```
Generate the C++ class:

```bash
titanium-proto -fp example.json
```
The above command creates a C++ class ExamplePackageProto with methods for accessing, serializing, and deserializing fields.
Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
 ## License

This project is licensed under the MIT License - see the LICENSE file for details.
