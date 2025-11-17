import re
import pefile


def read_file_chunk(path: str, size: int = 64 * 1024) -> bytes:
    with open(path, "rb") as f:
        return f.read(size)


def extract_ascii_strings(data: bytes, limit: int = 100) -> list[str]:
    ascii_strings = re.findall(rb"[\x20-\x7E]{4,}", data)
    return [s.decode("ascii", errors="ignore") for s in ascii_strings[:limit]]


def parse_pe_info(path: str) -> dict:
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories()
    return {
        "sections": [
            {
                "name": sec.Name.decode(errors="ignore").rstrip("\x00"),
                "virtual_size": sec.Misc_VirtualSize,
                "raw_size": sec.SizeOfRawData,
                "entropy": sec.get_entropy(),
            }
            for sec in pe.sections
        ],
        "imports": [
            imp.name.decode() if imp.name else ""
            for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", [])
            for imp in entry.imports
        ],
        "exports": [
            exp.name.decode() if exp.name else ""
            for exp in getattr(pe, "DIRECTORY_ENTRY_EXPORT", []).symbols
        ],
        "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
        "dll_characteristics": pe.OPTIONAL_HEADER.DllCharacteristics,
    }
