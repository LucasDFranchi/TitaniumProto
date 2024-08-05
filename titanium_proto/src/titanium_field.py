class TitaniumField:
    _SINGLE_BLOCK = 1

    def __init__(self, field_dict: dict):
        """
        Initialize a TitaniumField instance.

        Args:
            field_dict (dict): A dictionary containing field information.
                               Expected keys are 'type', 'name', and optionally 'maximum_size'.
        """
        self._type_name = field_dict.get("type")
        self._variable_name = field_dict.get("name")
        self._block_size = field_dict.get("maximum_size", self._SINGLE_BLOCK)
        self._token_id = field_dict.get("token_id")

        if self._type_name == "string" and self._block_size <= self._SINGLE_BLOCK:
            raise ValueError(
                f"Invalid block size for string field '{self._variable_name}': should be greater than {self._SINGLE_BLOCK}."
            )

    def _to_pascal_case(self, snake_str: str) -> str:
        """
        Converts a snake_case string to PascalCase.

        Args:
            snake_str (str): The snake_case string to convert.

        Returns:
            str: The converted PascalCase string.
        """
        components = snake_str.split("_")
        return "".join(x.title() for x in components)

    def to_dict(self):
        field_dict = {}
        field_dict["internal_name"] = self.internal_name
        field_dict["is_array"] = self.is_array
        field_dict["c_type_name"] = self.c_type_name
        field_dict["capitalized_name"] = self.capitalized_name
        field_dict["defined_size"] = self.defined_size
        field_dict["size"] = self.size
        field_dict["token_name"] = self.token_name
        field_dict["c_to_struct"] = self.c_to_struct

        return field_dict

    @property
    def c_type_name(self):
        """
        Returns the C equivalent type name. Converts 'string' to 'char'.

        Returns:
            str: The C type name.
        """
        return self._type_name if self._type_name != "string" else "char"

    @property
    def type_name(self):
        """
        Returns the type name of the field.

        Returns:
            str: The type name.
        """
        return self._type_name

    @property
    def is_array(self):
        """
        Checks if the field is an array based on block size.

        Returns:
            bool: True if the block size is greater than a single block, False otherwise.
        """
        return int(self._block_size) > self._SINGLE_BLOCK

    @property
    def size(self):
        """
        Returns the block size of the field.

        Returns:
            int: The block size.
        """
        return self._block_size

    @property
    def internal_name(self):
        """
        Returns the internal name of the field, prefixed with an underscore.

        Returns:
            str: The internal name.
        """
        return f"_{self._variable_name}"

    @property
    def token_name(self):
        return f"{self._variable_name}"

    @property
    def capitalized_name(self):
        """
        Returns the capitalized variable name of the field.

        Returns:
            str: The capitalized variable name.
        """
        return f"{self._to_pascal_case(self._variable_name)}"

    @property
    def defined_size(self):
        """
        Returns the defined size name of the field in uppercase.

        Returns:
            str: The defined size name.
        """
        return f"{self._variable_name.upper()}_SIZE" if self.is_array else None

    @property
    def c_to_struct(self):
        c_to_struct = {
            "uint8_t": "B",
            "int8_t": "b",
            "uint16_t": "H",
            "int16_t": "h",
            "uint32_t": "I",
            "int32_t": "i",
            "uint64_t": "Q",  
            "int64_t": "q",
            "char": "c",
        }

        return c_to_struct.get(self.c_type_name)

    @property
    def maximum_field_length(self):
        type_ranges = {
            "uint8_t": "255",
            "uint16_t": "65535",
            "uint32_t": "4294967295",
            "uint64_t": "18446744073709551615",
            "int8_t": "-127",
            "int16_t": "-32767",
            "int32_t": "-2147483647",
            "int64_t": "-9223372036854775807",
        }

        maximum_str = None

        if self._type_name == "string":
            maximum_str = "-" * self._block_size
        else:
            maximum_str = type_ranges.get(self.c_type_name)

        return maximum_str
