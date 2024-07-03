import json

from .titanium_field import TitaniumField


class TitaniumProto:
    _SUPPORTED_TYPES = [
        "uint8_t",
        "int8_t",
        "uint16_t",
        "int16_t",
        "uint32_t",
        "int32_t",
        "uint64_t",
        "int64_t",
        "float",
        "double",
        "string",
    ]

    def __init__(self):
        """
        Initializes a new instance of the TitaniumProto class.
        """
        self._content = None
        self._package_name = None
        self._fields = []

    def _read_file(self, filepath: str):
        """
        Read content from a JSON file.

        Args:
            filepath (str): Path to the Titanium Protobuf JSON file.
        """
        with open(filepath, "r") as file:
            self._content = json.load(file)

    def _validate_syntax(self):
        """
        Validates the syntax of the protocol file.

        Raises:
            ValueError: If the syntax is not "titanium1".
        """
        if self._content.get("syntax") != "titanium1":
            raise ValueError(
                "Invalid syntax: protocol file must have 'syntax' set to 'titanium1'."
            )

    def _update_package_name(self):
        """
        Updates the package name by parsing the protocol file content.

        Raises:
            ValueError: If the package name is missing.
        """
        self._package_name = self._content.get("package")
        if self._package_name is None:
            raise ValueError("Missing Package Name in protocol file.")

    def _parse_fields(self):
        """
        Parse and validate fields from the protocol file content.

        Raises:
            ValueError: If a field has an unsupported data type.
        """
        for field in self._content.get("fields"):
            field_type = field.get("type")
            if field_type not in self._SUPPORTED_TYPES:
                supported_types_str = ", ".join(self._SUPPORTED_TYPES)
                raise ValueError(
                    f"Unsupported data type: {field_type}. Supported types are: {supported_types_str}."
                )

            self._fields.append(TitaniumField(field))

    def _generate_includes(self):
        """
        Generates C++ include statements for necessary headers.

        Returns:
            str: A string containing include statements for 'stdint.h' and 'string.h'.
        """
        method_str = '#include "stdint.h"\n' '#include "string.h"\n\n'

        return method_str

    def _generate_errors_namespace(self):
        """
        Generates a C++ namespace for error codes.

        Returns:
            str: A string containing error codes within a 'Errors' namespace.
        """
        method_str = (
            "namespace Errors {\n"
            "    constexpr int8_t NO_ERROR = 0;\n"
            "    constexpr int8_t INVALID_BUFFER_PTR = -1;\n"
            "    constexpr int8_t INVALID_BUFFER_SIZE = -2;\n"
            "    constexpr int8_t OVERFLOW_BUFFER = -3;\n"
            "}\n\n"
        )

        return method_str

    def _generate_classname(self):
        """
        Generates a C++ class definition based on the package name.

        Returns:
            str: A string containing a C++ class definition with default constructor and destructor.
        """
        method_str = (
            f"class {self._package_name}Protobuf {{\n"
            f"public:\n"
            f"    {self._package_name}Protobuf() = default;\n"
            f"    ~{self._package_name}Protobuf() = default;\n\n"
        )

        return method_str

    def _generate_public_methods(self):
        """
        Generates public methods for accessing and manipulating Titanium protobuf fields.

        Returns:
            str: A string containing C++ code for all generated public methods.
        """
        public_methods_string = ""

        for titanium_field in self._fields:
            public_methods_string += self._generate_block_size_variables(titanium_field)
        public_methods_string += "\n"
        for titanium_field in self._fields:
            public_methods_string += self._generate_get_methods(titanium_field)
        public_methods_string += "\n"

        for titanium_field in self._fields:
            public_methods_string += self._generate_update_methods(titanium_field)

        public_methods_string += self._generate_serialize_method()
        public_methods_string += "\n\n"
        public_methods_string += self._generate_deserialize_method()
        public_methods_string += "\n\n"

        return public_methods_string

    def _generate_private_variables_end_block(self):
        """
        Generates private variables and ends the class block.

        Returns:
            str: A string containing private variable declarations for each field followed by the class block end.
        """
        end_string = "private:\n"

        for titanium_field in self._fields:
            end_string += self._generate_private_variables(titanium_field)

        end_string += "};"

        return end_string

    def _generate_block_size_variables(self, titanium_field: TitaniumField):
        """
        Generates block size define variables for array fields.

        Args:
            titanium_field (TitaniumField): The TitaniumField object representing the field.

        Returns:
            str: A string containing the constexpr definition of the block size variable, or an empty string if not applicable.
        """
        define_block_size_str = ""

        if titanium_field.is_array:
            define_block_size_str = f"    static constexpr uint16_t {titanium_field.defined_size} = {titanium_field.size};\n"

        return define_block_size_str

    def _generate_get_methods(self, titanium_field: TitaniumField):
        """
        Generates getter methods for accessing field values.

        Args:
            titanium_field (TitaniumField): The TitaniumField object representing the field.

        Returns:
            str: A string containing the C++ code for the getter method.
        """
        get_method_str = ""

        if titanium_field.is_array:
            get_method_str = f"    const {titanium_field.c_type_name}* Get{titanium_field.capitalized_name}(void) const {{  return this->{titanium_field.internal_name}; }}\n"
        else:
            get_method_str = f"    {titanium_field.c_type_name} Get{titanium_field.capitalized_name}(void) const {{  return this->{titanium_field.internal_name}; }}\n"

        return get_method_str

    def _generate_update_methods(self, titanium_field: TitaniumField):
        """
        Generates and prints the update methods for a TitaniumField.

        Args:
            titanium_field (TitaniumField): The TitaniumField object for which to generate update methods.
        """
        if titanium_field.is_array:
            method_str = (
                f"    int8_t Update{titanium_field.capitalized_name}({titanium_field.c_type_name}* value) {{\n"
                f"        if (value == nullptr || this->{titanium_field.internal_name} == nullptr) {{\n"
                f"            return Errors::INVALID_BUFFER_PTR;\n"
                f"        }}\n\n"
                f"        size_t value_length = strlen(value) + 1;\n\n"
                f"        if ((value_length == 0) || {titanium_field.defined_size} == 0) {{\n"
                f"            return Errors::INVALID_BUFFER_SIZE;\n"
                f"        }}\n\n"
                f"        if (value_length > {titanium_field.defined_size}) {{\n"
                f"            return Errors::OVERFLOW_BUFFER;\n"
                f"        }}\n\n"
                f"        memset(this->{titanium_field.internal_name}, 0, {titanium_field.defined_size});\n"
                f"        memcpy(this->{titanium_field.internal_name}, value, value_length);\n\n"
                f"        return Errors::NO_ERROR;\n"
                f"    }}\n\n"
            )
        else:
            method_str = (
                f"    int8_t Update{titanium_field.capitalized_name}({titanium_field.c_type_name} value) {{\n"
                f"        this->{titanium_field.internal_name} = value;\n"
                f"        return Errors::NO_ERROR;\n"
                f"    }}\n\n"
            )

        return method_str

    def _generate_serialize_method(self):
        """
        Generates a C++ method for serializing object data into a buffer.

        Returns:
            str: A string containing the C++ code for the Serialize method.
        """
        field_size_list = []
        for index, field in enumerate(self._fields):
            if field.type_name == "string":
                field_size_list.append(f"(strlen(this->{field.internal_name}) + 1)")
            else:
                field_size_list.append(f"sizeof(this->{field.internal_name})")

            fields_size_code = " + ".join(field_size_list)

        method_str = (
            "    int16_t Serialize(char* out_buffer, uint16_t out_buffer_size) const {\n"
            f"        if (out_buffer == nullptr) {{\n"
            f"            return 0;\n"
            f"        }}\n\n"
            f"        uint16_t serialized_size = {fields_size_code};\n\n"
            f"        if (out_buffer_size < serialized_size) {{\n"
            f"            return 0;\n"
            f"        }}\n\n"
        )

        method_str += f"        uint16_t offset = 0;\n\n"
        for index, field in enumerate(self._fields):
            if field.type_name == "string":
                field_size = f"strlen(this->{field.internal_name}) + 1"
            else:
                field_size = f"sizeof(this->{field.internal_name})"

            field_name = (
                f"this->{field.internal_name}"
                if field.is_array
                else f"&this->{field.internal_name}"
            )
            method_str += (
                f"        memcpy(&out_buffer[offset], {field_name}, {field_size});\n"
            )
            if index != (len(self._fields) - 1):
                method_str += f"        offset += {field_size};\n"

        method_str += "    \n        return serialized_size;\n    }"

        return method_str

    def _generate_deserialize_method(self):
        """
        Generates a C++ method for deserializing object data from a buffer.

        Returns:
            str: A string containing the C++ code for the DeSerialize method.
        """
        field_size_list = []
        for index, field in enumerate(self._fields):
            if field.type_name == "string":
                field_size_list.append(f"1")
            else:
                field_size_list.append(f"sizeof(this->{field.internal_name})")

            fields_size_code_min = " + ".join(field_size_list)

        fields_size_code_max = " + ".join(
            [f"sizeof(this->{field.internal_name})" for field in self._fields]
        )

        method_str = (
            "    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {\n"
            f"        if (in_buffer == nullptr) {{\n"
            f"            return Errors::INVALID_BUFFER_PTR;\n"
            f"        }}\n\n"
            f"        uint16_t deserialized_min_size = {fields_size_code_min};\n"
            f"        uint16_t deserialized_max_size = {fields_size_code_max};\n\n"
            f"        if (in_buffer_size < deserialized_min_size) {{\n"
            f"            return Errors::OVERFLOW_BUFFER;\n"
            f"        }}\n\n"
            f"        if (in_buffer_size > deserialized_max_size) {{\n"
            f"            return Errors::OVERFLOW_BUFFER;\n"
            f"        }}\n\n"
        )

        for value in self._fields:
            if value.is_array:
                method_str += f"        memset(this->{value.internal_name}, 0, {value.defined_size});\n"

        method_str += f"\n        uint16_t offset = 0;\n"
        for index, field in enumerate(self._fields):
            if field.type_name == "string":
                field_size_code = f"strlen(&in_buffer[offset]) + 1"
            else:
                field_size_code = f"sizeof(this->{field.internal_name})"

            field_name = (
                f"this->{field.internal_name}"
                if field.is_array
                else f"&this->{field.internal_name}"
            )
            method_str += f"        memcpy({field_name}, &in_buffer[offset], {field_size_code});\n"
            if index != (len(self._fields) - 1):
                method_str += f"        offset += {field_size_code};\n"

        method_str += "    \n        return Errors::NO_ERROR;\n    }"

        return method_str

    def _generate_private_variables(self, titanium_field: TitaniumField):
        """
        Generates a private member variable declaration for a TitaniumField.

        Args:
            titanium_field (TitaniumField): The TitaniumField object representing the field.

        Returns:
            str: A string containing the C++ code for declaring the private member variable.
        """
        if titanium_field.is_array:
            method_str = f"    {titanium_field.c_type_name} {titanium_field.internal_name}[{titanium_field.size}] = {{0}};\n"
        else:
            method_str = f"    {titanium_field.c_type_name} {titanium_field.internal_name} = 0;\n"

        return method_str

    def import_and_parse_proto_file(self, filepath: str):
        """
        Imports and parses definitions from a Titanium protobuf file.

        Args:
            filepath (str): Path to the Titanium protobuf file.
        
        Raises:
            ValueError: If there are syntax errors in the protobuf file or required fields are missing.
        """
        self._read_file(filepath)
        self._validate_syntax()
        self._update_package_name()
        self._parse_fields()
        
    def generate_cpp_file(self, redirect_outfile: str = ""):
        """
        Generates a C++ source file based on the current object's state and writes it to disk.

        This method generates a complete C++ source file by combining several generated sections:
        includes, error namespace, class definition, public methods, and private variables. It then 
        writes this content to a file named after the package name of the object.
        
        Args:
            redirect_outfile (str): Add additional arguments to redirect the generated file.

        Raises:
            IOError: If there is an issue writing to the file.

        """
        file_str = ""
        
        file_str = self._generate_includes()
        file_str += self._generate_errors_namespace()
        file_str += self._generate_classname()
        file_str += self._generate_public_methods()
        file_str += self._generate_private_variables_end_block()
        
        with open(f"{redirect_outfile}{self._package_name}.cpp", 'w') as file:
            file.write(file_str)