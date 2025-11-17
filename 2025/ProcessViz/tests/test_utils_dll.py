import pytest
from unittest.mock import patch, MagicMock
from app.utils import utils_dll


def test_read_file_chunk(tmp_path):
    file_path = tmp_path / "test.bin"
    content = b"ABCDE" * 100
    file_path.write_bytes(content)

    chunk = utils_dll.read_file_chunk(str(file_path), size=10)
    assert chunk == content[:10]


def test_extract_ascii_strings_basic():
    data = b"abc\x00defghi1234\x7f!@#"
    strings = utils_dll.extract_ascii_strings(data, limit=10)
    assert "defghi1234" in strings


def test_extract_ascii_strings_limit():
    data = b"AAAA\x00BBBB\x00CCCC"
    strings = utils_dll.extract_ascii_strings(data, limit=2)
    assert len(strings) == 2
    assert strings == ["AAAA", "BBBB"]


@patch("app.utils.utils_dll.pefile.PE")
def test_parse_pe_info_sections_imports_exports(mock_pe):
    mock_section = MagicMock()
    mock_section.Name = b".text\x00"
    mock_section.Misc_VirtualSize = 1000
    mock_section.SizeOfRawData = 500
    mock_section.get_entropy.return_value = 7.5
    mock_pe_instance = MagicMock()
    mock_pe_instance.sections = [mock_section]
    mock_pe_instance.OPTIONAL_HEADER.AddressOfEntryPoint = 0x1234
    mock_pe_instance.OPTIONAL_HEADER.DllCharacteristics = 0x40
    # Mock imports/exports
    mock_import = MagicMock()
    mock_import.name = b"ImportFunc"
    mock_export = MagicMock()
    mock_export.name = b"ExportFunc"
    mock_pe_instance.DIRECTORY_ENTRY_IMPORT = [MagicMock(imports=[mock_import])]
    mock_pe_instance.DIRECTORY_ENTRY_EXPORT = MagicMock(symbols=[mock_export])
    mock_pe.return_value = mock_pe_instance

    info = utils_dll.parse_pe_info("dummy.dll")

    # Vérifications basiques
    assert info["sections"][0]["name"] == ".text"
    assert info["sections"][0]["virtual_size"] == 1000
    assert info["sections"][0]["raw_size"] == 500
    assert info["sections"][0]["entropy"] == 7.5
    assert info["imports"] == ["ImportFunc"]
    assert info["exports"] == ["ExportFunc"]
    assert info["entry_point"] == hex(0x1234)
    assert info["dll_characteristics"] == 0x40
