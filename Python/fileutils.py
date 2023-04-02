from __future__ import annotations
import io
import os
from typing import TextIO


class FileEncodingException(Exception):
    pass


class FileHandler():
    def __init__(self, encodings: tuple = ('utf-8', 'utf-16', 'utf-32')):
        self.encodings = encodings
        self.file_handles = {}

    def detect_file_encoding(self, path: str | os.PathLike) -> str:
        for encoding in self.encodings:
            f = open(path, 'r', encoding=encoding)
            try:
                f.read()
            except UnicodeDecodeError:
                pass
            else:
                return encoding
            finally:
                f.close()
        raise FileEncodingException(f"Failed to detect encoding of file {path}")

    def open_file(self, path: str | os.PathLike, mode: str, encoding=None) -> \
            TextIO | io.TextIOWrapper | io.BufferedReader:
        if not (encoding or 'b' in mode):
            # Auto-detect encoding
            encoding = self.detect_file_encoding(path)
        return open(path, mode, encoding=encoding)

    def create_file_handle(self, path: str | os.PathLike, mode: str, encoding=None, name: str = None) -> \
            TextIO | io.TextIOWrapper | io.BufferedReader:
        if not name:
            name = path
        handle = self.open_file(path, mode, encoding=encoding)
        self.file_handles[name] = handle
        return handle

    def get_file_handle(self, name) -> TextIO | io.TextIOWrapper | io.BufferedReader:
        return self.file_handles[name]

    def close_file_handle(self, name) -> FileHandler:
        self.file_handles[name].close()
        del self.file_handles[name]
        return self

    def close_all_file_handles(self) -> FileHandler:
        self.file_handles.clear()
        return self

    def read_file(self, path: str | os.PathLike, encoding=None, binary=False) -> str | bytes:
        if binary:
            with self.open_file(path, 'rb') as f:
                return f.read()
        else:
            with self.open_file(path, 'r', encoding) as f:
                return f.read()

    def read_bytes(self, path: str | os.PathLike, hex=True, hexformat: Optional[Callable] = None) -> \
            bytes | str:
        filecontent = self.read_file(path, binary=True)
        if hex:
            if hexformat:
                return hexformat(filecontent.hex())
            else:
                return filecontent.hex()
        else:
            return filecontent

    def write_file(self, path: str | os.PathLike, data: str | bytes, encoding, binary=False) -> \
            TextIO | io.TextIOWrapper | io.BufferedReader | str:
        with self.open_file(path, encoding, binary) as f:
            f.write(data)
            return f


f = FileHandler()
print(f.read_file(r"C:\Users\zachy\Downloads\Configuration.lua"))