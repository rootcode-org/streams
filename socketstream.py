# Copyright is waived. No warranty is provided. Unrestricted use and modification is permitted.

"""
Read/Write a stream of bytes from/to a socket
"""

from stream import Stream


class SocketStream(Stream):

    def __init__(self, socket):
        Stream.__init__(self)
        self.socket = socket
        self.write_buffer = bytearray()
        self.read_buffer = bytearray()
        self.read_buffer_length = 0
        self.read_position = 0

    def close(self):
        self.socket.close()

    def read_seek(self, offset):
        if offset < 0:
            raise ValueError("Backwards seek is not supported")
        self.read_position += offset

    def read_u8(self):
        return self.read_u8_array(1)[0]

    def read_u8_array(self, length, read_ahead=16384):
        if self.read_position + length > len(self.read_buffer):
            self.read_buffer = self.read_buffer[self.read_position:] + self.socket.recv(length + read_ahead)
            self.read_position = 0
        data = self.read_buffer[self.read_position:self.read_position + length]
        self.read_position += length
        return data

    def write_u8(self, value):
        self.write_buffer.append(value)
        self.length += 1

    def write_u8_array(self, data):
        self.write_buffer += data
        self.length += len(data)

    def get_write_buffer(self):
        return self.write_buffer

    def flush(self):
        self.socket.sendall(self.write_buffer)
        self.write_buffer = bytearray()
        self.length = 0
