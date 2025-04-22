import string
from typing import List
import os


def is_ascii_printable(
    filepath: str, nontext_ratio: float, blocksize: int = 512
) -> bool:
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(blocksize)
            if not chunk:
                return True
            text_chars = bytes(string.printable, "ascii")
            nontext_ratio = sum(1 for b in chunk if b not in text_chars) / len(chunk)
            return nontext_ratio < nontext_ratio
    except Exception as e:
        print(f"Error reading file: {e}")
        return False


def is_text_utf8(filepath: str, blocksize: int = 512) -> bool:
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(blocksize)
            chunk.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False


def is_plaintext(filepath: str) -> bool:
    return is_ascii_printable(filepath, 0.3) or is_text_utf8(filepath)


def list_file_recursive(rootpath: str) -> List[str]:
    all_files = []
    for dirpath, _, filenames in os.walk:
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            all_files.append(filepath)
    return all_files


def list_plaintext_file(rootpath: str) -> List[str]:
    plaintext_file = []
    all_files = list_file_recursive(rootpath)
    for filepath in all_files:
        if is_plaintext(filepath):
            plaintext_file.append(filepath)
    return plaintext_file


def dump_plaintext_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading file {e}")
        return False
