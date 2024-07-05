import json
import shutil
import pytest

from unittest.mock import mock_open, patch

from titanium_proto.src import TitaniumFileGenerator
from titanium_proto.src import TitaniumField

@pytest.fixture
def temp_dir(tmp_path):
    # Setup: create a temporary directory
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    
    yield dir_path
    
    # Teardown: clear the temporary directory
    shutil.rmtree(dir_path)

def test_read_file():
    tp = TitaniumFileGenerator()
    mock_data = json.dumps({"syntax": "titanium1", "package": "testpkg", "fields": []})
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        tp._read_file("dummy_path")
        mock_file.assert_called_with("dummy_path", "r")
        assert tp._content == json.loads(mock_data)

def test_validate_syntax_valid():
    tp = TitaniumFileGenerator()
    tp._content = {"syntax": "titanium1"}
    tp._validate_syntax()

def test_validate_syntax_invalid():
    tp = TitaniumFileGenerator()
    tp._content = {"syntax": "invalid_syntax"}
    with pytest.raises(ValueError, match="Invalid syntax: protocol file must have 'syntax' set to 'titanium1'."):
        tp._validate_syntax()

def test_update_package_name():
    tp = TitaniumFileGenerator()
    tp._content = {"package": "testpkg"}
    tp._update_package_name()
    assert tp._package_name == "testpkg"

def test_update_package_name_missing():
    tp = TitaniumFileGenerator()
    tp._content = {}
    with pytest.raises(ValueError, match="Missing Package Name in protocol file."):
        tp._update_package_name()

def test_parse_fields_valid():
    tp = TitaniumFileGenerator()
    tp._content = {
        "fields": [
            {"name": "field1", "type": "uint8_t"},
            {"name": "field2", "type": "float"},
            {"name": "field3", "type": "string", "maximum_size": 128},
        ]
    }
    tp._parse_fields()
    assert len(tp._fields) == 3
    assert isinstance(tp._fields[0], TitaniumField)
    assert tp._fields[0].internal_name == "_field1"
    assert tp._fields[0].capitalized_name == "Field1"
    assert tp._fields[0].defined_size == None
    assert tp._fields[0].type_name == "uint8_t"
    assert tp._fields[0].size == 1
    assert isinstance(tp._fields[1], TitaniumField)
    assert tp._fields[1].internal_name == "_field2"
    assert tp._fields[1].capitalized_name == "Field2"
    assert tp._fields[1].defined_size == None
    assert tp._fields[1].type_name == "float"
    assert tp._fields[1].size == 1
    assert isinstance(tp._fields[2], TitaniumField)
    assert tp._fields[2].internal_name == "_field3"
    assert tp._fields[2].capitalized_name == "Field3"
    assert tp._fields[2].defined_size == "FIELD3_SIZE"
    assert tp._fields[2].type_name == "string"
    assert tp._fields[2].size == 128
    
def test_parse_fields_invalid_type():
    tp = TitaniumFileGenerator()
    tp._content = {
        "fields": [
            {"name": "field1", "type": "unsupported_type"},
        ]
    }
    with pytest.raises(ValueError, match="Unsupported data type: unsupported_type. Supported types are: "):
        tp._parse_fields()

def test_generate_header_file(temp_dir):   
    tp = TitaniumFileGenerator()
    tp.import_and_parse_proto_file("./tests/resources/test.json")
    tp.generate_header_file(f"{temp_dir}/")
    
    with open(f"{temp_dir}/TestProto.h", 'r') as generated_cpp_file:
        generated_cpp_content = generated_cpp_file.read()
        
    with open("./tests/resources/valid_cpp_content.h", 'r') as generated_cpp_file:
        expected_cpp_content = generated_cpp_file.read()
        
    assert generated_cpp_content == expected_cpp_content


if __name__ == "__main__":
    pytest.main()
