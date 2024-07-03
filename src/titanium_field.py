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
    def capitalized_name(self):
        """
        Returns the capitalized variable name of the field.

        Returns:
            str: The capitalized variable name.
        """
        return f"{self._variable_name.capitalize()}"

    @property
    def defined_size(self):
        """
        Returns the defined size name of the field in uppercase.

        Returns:
            str: The defined size name.
        """
        return f"{self._variable_name.upper()}_SIZE" if self.is_array else None
