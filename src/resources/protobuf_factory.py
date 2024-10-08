from .titanium_pb2 import *
from google.protobuf.descriptor import FieldDescriptor

class ProtobufFactory:
    """
    A factory class for creating instances of protobuf message types.

    This class provides a method to instantiate specific protobuf messages
    based on a given index, which corresponds to the defined memory areas
    in the protobuf definitions. The factory uses the descriptor information
    to dynamically create the appropriate message type.

    Attributes:
        memory_area_dict (dict): A dictionary mapping memory area names
        to their corresponding indices.
    """
    memory_area_dict = {
        key: x.number for key, x in MemoryAreas.DESCRIPTOR.values_by_name.items()
    }

    @classmethod
    def create_instance(cls, index: int):
        """
        Creates an instance of a protobuf message based on the given index.

        Args:
            index (int): The index corresponding to the desired protobuf message type.

        Raises:
            ValueError: If the provided index does not match any valid memory area.

        Returns:
            The instantiated protobuf message object corresponding to the index,
            or None if no matching index is found.
        """
        if index not in cls.memory_area_dict.values():
            raise ValueError(
                f"Unsupported Memory Area! Valid options are: {list(cls.memory_area_dict.values())}"
            )
        
        memory_areas_definitions = MemoryAreasDefinitions()
        descriptor_object = memory_areas_definitions.DESCRIPTOR
        
        for field in descriptor_object.fields:
            if field.number == index:
                return globals()[field.message_type.name]()
        
        return None