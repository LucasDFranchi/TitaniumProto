import json

from jinja2 import Template

from .titanium_field import TitaniumField
from .cpp_template import template_cpp_string
from .python_template import template_python_string

class TitaniumFileGenerator:
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

    def __init__(self, output_extension: str):
        """
        Initializes a new instance of the TitaniumProto class.
        """
        self._content = None
        self._package_name = None
        self._fields = []
        self._output_extension = output_extension

        if self._output_extension == "h":
            self._template = Template(template_cpp_string)
        elif self._output_extension == "py":
            self._template = Template(template_python_string)

    def _read_file(self, filepath: str):
        """
        Read content from a JSON file.

        Args:
            filepath (str): Path to the Titanium Protobuf JSON file.
        """
        with open(filepath, "r") as file:
            self._content = json.load(file)

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
        token_id = 1
        for field in self._content.get("fields"):
            field_type = field.get("type")
            field["token_id"] = token_id
            if field_type not in self._SUPPORTED_TYPES:
                supported_types_str = ", ".join(self._SUPPORTED_TYPES)
                raise ValueError(
                    f"Unsupported data type: {field_type}. Supported types are: {supported_types_str}."
                )

            self._fields.append(TitaniumField(field))
            token_id += 2

    def _unpack_string(self):
        unpack_string = ""

        for field in self._fields:
            if field._type_name == "string":
                unpack_string += "{}s "
            else:
                unpack_string += f"{field.c_to_struct} "

        return unpack_string


    def import_and_parse_proto_file(self, filepath: str = None, raw_data: str = None):
        """
        Imports and parses definitions from a Titanium protobuf file.

        Args:
            filepath (str): Path to the Titanium protobuf file.
        
        Raises:
            ValueError: If there are syntax errors in the protobuf file or required fields are missing.
        """
        if filepath:
            self._read_file(filepath)
        else:
            self._content = raw_data

        self._update_package_name()
        self._parse_fields()
        
    def generate_header_file(self, redirect_outfile: str = "", enable_json: bool = False):
        data = {}
        maximum_json_size = {}
        serialized_size_list = []
        maximum_size_list = []
        minimum_size_list = []
        static_maximum_size_list = []
        num_of_arrays = 0
        
        data["package_name"] = self._package_name
        data["fields"] = []
        for field in self._fields:
            # json_size += field.maximum_json_size
            maximum_json_size[field.token_name] = field.maximum_field_length
            data["fields"].append(field.to_dict())
            
            if field.is_array:
                serialized_size_list.append(f"strlen(this->{field.internal_name})")
                static_maximum_size_list.append(f"{field.defined_size}")
                num_of_arrays += 1
            else:
                serialized_size_list.append(f"sizeof(this->{field.internal_name})")
                static_maximum_size_list.append(f"sizeof({field.type_name})")
                minimum_size_list.append(f"sizeof(this->{field.internal_name})")
                
            maximum_size_list.append(f"sizeof(this->{field.internal_name})")

        data["proto"] = {}            
        data["proto"]["serialized_size"] =  " + ".join(serialized_size_list) + f" + {len(self._fields)}"
        data["proto"]["maximum_size"] = " + ".join(maximum_size_list)
        data["proto"]["minimum_size"] = " + ".join(minimum_size_list) + f" + {num_of_arrays}"
        data["proto"]["static_maximum_size"] = " + ".join(static_maximum_size_list)
        data["proto"]["json_enable"] = enable_json
        data["proto"]["num_var"] = len(self._fields)
        data["proto"]["json_size"] = 512
        data["proto"]["unpack_string"] = self._unpack_string()
        
        rendered_code = self._template.render(data)
            
        with open(f"{redirect_outfile}{self._package_name}Proto.{self._output_extension}", 'w') as file:
            file.write(rendered_code)