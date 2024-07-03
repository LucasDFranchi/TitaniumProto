import argparse
import json

def handle_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="This script is used to run inventory and collect data from it"
    )

    parser.add_argument("--file_path", "-fp", help="Path to Titanium Protobuf file", required=True)

    return parser.parse_args()

class TitaniumField:
    _SINGLE_BLOCK = 1
    
    def __init__(self, field_dict: dict):
        
        self._type_name = field_dict.get("type")
        self._variable_name = field_dict.get("name")
        self._block_size = field_dict.get("maximum_size", self._SINGLE_BLOCK)
    
    @property
    def c_type_name(self):
        return self._type_name if self._type_name != "string" else "char"

    @property
    def type_name(self):
        return self._type_name
    
    @property
    def is_array(self):
        return int(self._block_size) > self._SINGLE_BLOCK
        
    @property
    def size(self):
        return self._block_size
        
    @property
    def internal_name(self):
        return f"_{self._variable_name}"
    
    @property
    def capitalized_name(self):
        return f"{self._variable_name.capitalize()}"
    
    @property
    def defined_size(self):
        return f"{self._variable_name.upper()}_SIZE"

class TitaniumProto:
    _SYNTAX_LINE = 0
    _SUPPORTED_TYPES = ["uint8_t", "int8_t", "uint16_t", "int16_t", "uint32_t", "int32_t", "uint64_t", "int64_t", "float", "double", "string"]
    
    def __init__(self):
        """
        Initializes a new instance of the TitaniumProto class.
        """
        self._content = None
        self._package_name = None
        self._fields = []
    
    def _read_file(self, filepath: str):
        with open(filepath, 'r') as file:
            self._content = json.load(file)
            
    def _validate_syntax(self):
        """
        Validates the syntax of the protocol file.

        Returns:
            bool: True if the syntax is "titanium1", False otherwise.
        """
        if self._content.get("syntax") != "titanium1":
            raise Exception("Invalid syntax!")
    
    def _update_package_name(self):
        """
        Updates the package name by parsing the protocol file content.

        Raises:
            Exception: If the package name is missing.
        """
        self._package_name = self._content.get("package")
        if self._package_name is None:
            raise Exception("Missing Package Name!")
        
    def _parse_fields(self):
        for field in self._content.get("fields"):
            if field.get("type") not in self._SUPPORTED_TYPES:
                error_message = f"Error: Data type is not supported: {field.get("type")}. Supported types are: " + ", ".join(self._SUPPORTED_TYPES) + "."
                raise Exception(error_message)
            
            self._fields.append(TitaniumField(field))

    def read_proto_file(self, filepath):
        self._read_file(filepath)
        self._validate_syntax()
        self._update_package_name()
        self._parse_fields()
        
    def generate_includes(self):
        method_str = (
        '#include "stdint.h"\n'
        '#include "string.h"\n\n')
        
        return method_str
    
    def generate_errors_namespace(self):
        method_str = (
        "namespace Errors {\n"
        "    constexpr int8_t NO_ERROR = 0;\n"
        "    constexpr int8_t INVALID_BUFFER_PTR = -1;\n"
        "    constexpr int8_t INVALID_BUFFER_SIZE = -2;\n"
        "    constexpr int8_t OVERFLOW_BUFFER = -3;\n"
        "}\n\n")
        
        return method_str
    
    def generate_classname(self):
        method_str = (
            f"class {self.package_name}Protobuf {{\n"
            f"public:\n"
            f"    {self.package_name}Protobuf() = default;\n"
            f"    ~{self.package_name}Protobuf() = default;\n\n")
        
        return method_str    
    
    def generate_public_methods(self):
        public_methods_string = ""
        for titanium_field in self.fields:
            public_methods_string +=self._generate_block_size_variables(titanium_field)
        public_methods_string += "\n"
        for titanium_field in self.fields:
            public_methods_string += self._generate_get_methods(titanium_field)
        public_methods_string += "\n"
        for titanium_field in self.fields:
            public_methods_string += self._generate_update_methods(titanium_field)
        public_methods_string += self._generate_serialize_method()
        public_methods_string += "\n\n"
        public_methods_string += self._generate_deserialize_method()
        public_methods_string += "\n\n"
        
        return public_methods_string
    
    def generate_private_variables_end_block(self):
        end_string = "private:\n"
        
        for titanium_field in self.fields:
            end_string += self._generate_private_variables(titanium_field)
            
        end_string += "};"
        
        return end_string
    
    def _generate_block_size_variables(self, titanium_field: TitaniumField):
        if titanium_field.is_array:
            return f"    static constexpr uint16_t {titanium_field.defined_size} = {titanium_field.size};\n"
        return ""
    
    def _generate_get_methods(self, titanium_field: TitaniumField):
        if titanium_field.is_array:
            return f"    const {titanium_field.c_type_name}* Get{titanium_field.capitalized_name}(void) const {{  return this->{titanium_field.internal_name}; }}\n"
        else:
            return f"    {titanium_field.c_type_name} Get{titanium_field.capitalized_name}(void) const {{  return this->{titanium_field.internal_name}; }}\n"
        
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
        field_size_list = []
        for index, field in enumerate(self.fields):
            if field.type_name == "string":
                field_size_list.append(f"(strlen(this->{field.internal_name}) + 1)")
            else:
                field_size_list.append(f"sizeof(this->{field.internal_name})")

            fields_size_code = ' + '.join(field_size_list)
        
        method_str = ("    int16_t Serialize(char* out_buffer, uint16_t out_buffer_size) const {\n" + 
                      f"        if (out_buffer == nullptr) {{\n"
                      f"            return 0;\n"
                      f"        }}\n\n" +
                      f"        uint16_t serialized_size = {fields_size_code};\n\n" +
                      f"        if (out_buffer_size < serialized_size) {{\n"
                      f"            return 0;\n"
                      f"        }}\n\n")
        
        method_str += f"        uint16_t offset = 0;\n\n"
        for index, field in enumerate(self.fields):
            if field.type_name == "string":
                field_size = f"strlen(this->{field.internal_name}) + 1"
            else:
                field_size = f"sizeof(this->{field.internal_name})"
            
            field_name = f"this->{field.internal_name}" if field.is_array else f"&this->{field.internal_name}"
            method_str += (
                f"        memcpy(&out_buffer[offset], {field_name}, {field_size});\n"
            )
            if index != (len(self.fields) - 1):
                method_str +=    f"        offset += {field_size};\n"

        method_str += (
            "    \n"
            "        return serialized_size;\n"
            "    }"
        )

        return method_str
        
    def _generate_deserialize_method(self):
        field_size_list = []
        for index, field in enumerate(self.fields):
            if field.type_name == "string":
                field_size_list.append(f"1")
            else:
                field_size_list.append(f"sizeof(this->{field.internal_name})")

            fields_size_code_min = ' + '.join(field_size_list)
        
        fields_size_code_max = ' + '.join([f'sizeof(this->{field.internal_name})' for field in self.fields])
        
        method_str = ("    int8_t DeSerialize(const char* in_buffer, uint16_t in_buffer_size) {\n" + 
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
        
        for value in self.fields:
            if value.is_array:
                 method_str += (f"        memset(this->{value.internal_name}, 0, {value.defined_size});\n")
                 
        method_str += f"\n        uint16_t offset = 0;\n"
        for index, field in enumerate(self.fields):
            if field.type_name == "string":
                field_size_code = f"strlen(this->{field.internal_name}) + 1"
            else:
                field_size_code = f"sizeof(this->{field.internal_name})"
            
            field_name = f"this->{field.internal_name}" if field.is_array else f"&this->{field.internal_name}"
            method_str += (
                f"        memcpy({field_name}, &in_buffer[offset], {field_size_code});\n"
            )
            if index != (len(self.fields) - 1):
                method_str += f"        offset += {field_size_code};\n"
                 
        method_str += (
            "    \n"
            "        return Errors::NO_ERROR;\n"
            "    }"
        )
                 
        return method_str
                    
    def _generate_private_variables(self, titanium_field: TitaniumField):
        if titanium_field.is_array:
            method_str = f"    {titanium_field.c_type_name} {titanium_field.internal_name}[{titanium_field.size}] = {{0}};\n"
        else:
            method_str = f"    {titanium_field.c_type_name} {titanium_field.internal_name} = 0;\n"
            
        return method_str
            
    @property
    def package_name(self):
        return self._package_name
    
    @property
    def fields(self):
        return self._fields
            
def main():
    args = handle_arguments()
    
    tp = TitaniumProto()
    
    tp.read_proto_file(args.file_path)
    file_str = tp.generate_includes()
    file_str += tp.generate_errors_namespace()
    file_str += tp.generate_classname()
    
    file_str += tp.generate_public_methods()
    
    file_str += tp.generate_private_variables_end_block()
    
    print(file_str)

if __name__ == "__main__":
    main()
    