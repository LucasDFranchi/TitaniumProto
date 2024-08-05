import pytest
import struct
from .python._TestProto import _TestProtobuf  # Replace with the actual module name


class TestProtobufTestSuite:
    @pytest.fixture
    def proto(self):
        return _TestProtobuf()

    def test_update_first_field(self, proto):
        assert proto.update_first_field(42) == proto.PROTO_NO_ERROR
        assert proto.get_first_field() == 42

    def test_update_second_field(self, proto):
        assert proto.update_second_field(1234) == proto.PROTO_NO_ERROR
        assert proto.get_second_field() == 1234

    def test_update_third_field(self, proto):
        assert proto.update_third_field(567) == proto.PROTO_NO_ERROR
        assert proto.get_third_field() == 567

    def test_update_fourth_field_success(self, proto):
        assert proto.update_fourth_field("test") == proto.PROTO_NO_ERROR
        assert proto.get_fourth_field() == "test"

    def test_update_fourth_field_failures(self, proto):
        assert proto.update_fourth_field(None) == proto.PROTO_INVAL_PTR
        assert proto.update_fourth_field("") == proto.PROTO_OVERFLOW
        proto.FOURTH_FIELD_SIZE = 3
        assert proto.update_fourth_field("longer") == proto.PROTO_INVAL_SIZE

    def test_update_five_field(self, proto):
        assert proto.update_five_field(987654321) == proto.PROTO_NO_ERROR
        assert proto.get_five_field() == 987654321

    def test_serialize(self, proto):
        proto.update_first_field(1)
        proto.update_second_field(2)
        proto.update_third_field(3)
        proto.update_fourth_field("data")
        proto.update_five_field(4)

        out_buffer = bytearray(256)
        length = proto.serialize(out_buffer)
        
        assert length > 0
        assert out_buffer[:length] != b''

    def test_deserialize_success(self, proto):
        proto.update_first_field(1)
        proto.update_second_field(2)
        proto.update_third_field(3)
        proto.update_fourth_field("data")
        proto.update_five_field(4)

        out_buffer = bytearray(256)
        length = proto.serialize(out_buffer)
        
        new_proto = _TestProtobuf()
        assert new_proto.deserialize(out_buffer[:length]) == proto.PROTO_NO_ERROR
        assert new_proto.get_first_field() == 1
        assert new_proto.get_second_field() == 2
        assert new_proto.get_third_field() == 3
        assert new_proto.get_fourth_field() == "data"
        assert new_proto.get_five_field() == 4

    def test_deserialize_failure(self, proto):
        invalid_data = bytearray(b'\x00')  # Insufficient data

        new_proto = _TestProtobuf()
        assert new_proto.deserialize(invalid_data) == proto.PROTO_INVAL_PTR

    def test_serialize_json(self, proto):
        proto.update_first_field(1)
        proto.update_second_field(2)
        proto.update_third_field(3)
        proto.update_fourth_field("data")
        proto.update_five_field(4)

        out_buffer = bytearray(256)
        length = proto.serialize_json(out_buffer, len(out_buffer))
        
        assert length > 0
        assert b'first_field' in out_buffer

    def test_deserialize_json_success(self, proto):
        proto.update_first_field(1)
        proto.update_second_field(2)
        proto.update_third_field(3)
        proto.update_fourth_field("data")
        proto.update_five_field(4)

        out_buffer = bytearray(256)
        length = proto.serialize_json(out_buffer, len(out_buffer))
        
        new_proto = _TestProtobuf()
        assert new_proto.deserialize_json(out_buffer[:length]) == proto.PROTO_NO_ERROR
        assert new_proto.get_first_field() == 1
        assert new_proto.get_second_field() == 2
        assert new_proto.get_third_field() == 3
        assert new_proto.get_fourth_field() == "data"
        assert new_proto.get_five_field() == 4

    def test_deserialize_json_failures(self, proto):
        invalid_data = b'{"first_field": 1, "second_field": 2, "third_field": 3, "fourth_field": "data"}'

        new_proto = _TestProtobuf()
        assert new_proto.deserialize_json(invalid_data) == proto.PROTO_INVAL_JSON_KEY

        invalid_data = b'{"first_field": 1, "second_field": 2, "third_field": 3, "fourth_field": "data", "five_field": "string"}'
        assert new_proto.deserialize_json(invalid_data) == proto.PROTO_INVAL_JSON_VALUE