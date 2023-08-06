from __future__ import absolute_import

from collections import namedtuple
import gzip
import re
import struct

from . import compat


class Tag(object):
    _tags = {}
    _tuple = namedtuple("Tag", ["type", "name", "data"])

    def __init__(self, name, id_):
        self.name = name
        self.id = id_
        Tag._tags[id_] = self

    @classmethod
    def from_stream(cls, stream):
        return cls._tags[struct.unpack(">b", stream.read(1))[0]]

    def to_stream(self, stream):
        stream.write(struct.pack(">b", self.id))

    def parse(self, stream):
        name = TAG_String._parse_impl(stream)
        data = self._parse_impl(stream)
        return Tag._tuple(self, name, data)

    def dump(self, element, stream):
        type_, name, data = element
        type_.to_stream(stream)
        TAG_String._dump_impl(name, stream)
        self._dump_impl(data, stream)

    def _parse_length(self, length_type, stream):
        return struct.unpack(
            ">" + length_type.format, stream.read(length_type.size)
        )[0]

    def _dump_length(self, length_type, length, stream):
        stream.write(struct.pack(">" + length_type.format, length))

    def _parse_impl(self, stream):
        raise NotImplementedError()

    def _dump_impl(self, data, stream):
        raise NotImplementedError()

    def __repr__(self):
        return "TAG_%s" % re.sub(
            r"^(\w)|_(\w)", lambda m: m.group(0).upper(), self.name
        )


class FixedTag(Tag):
    def __init__(self, name, id_, size, format_):
        Tag.__init__(self, name, id_)
        self.size = size
        self.format = format_

    def _parse_impl(self, stream):
        return struct.unpack(">" + self.format, stream.read(self.size))[0]

    def _dump_impl(self, data, stream):
        stream.write(struct.pack(">" + self.format, data))


class EndTag(Tag):
    pass


class VariableTag(Tag):
    def __init__(self, name, id_, length_tag, encoding=None):
        Tag.__init__(self, name, id_)
        self.length_tag = length_tag
        self.encoding = encoding

    def _parse_impl(self, stream):
        length = self._parse_length(self.length_tag, stream)
        data = stream.read(length)
        if self.encoding:
            data = data.decode(self.encoding)
        return data

    def _dump_impl(self, data, stream):
        if self.encoding:
            data = data.encode(self.encoding)
        self._dump_length(self.length_tag, len(data), stream)
        stream.write(data)


class ListTag(Tag):
    def _parse_impl(self, stream):
        element_type = Tag.from_stream(stream)
        length = self._parse_length(TAG_Int, stream)

        return (
            element_type,
            [element_type._parse_impl(stream) for i in compat.range(length)],
        )

    def _dump_impl(self, data, stream):
        element_type, data = data
        element_type.to_stream(stream)
        self._dump_length(TAG_Int, len(data), stream)
        for elem in data:
            element_type._dump_impl(elem, stream)


class CompoundTag(Tag):
    def _parse_impl(self, stream):
        data = []
        while True:
            c_type_ = Tag.from_stream(stream)
            if c_type_ is TAG_End:
                break
            data.append(c_type_.parse(stream))
        return data

    def _dump_impl(self, data, stream):
        for elem in data:
            elem[0].dump(elem, stream)
        TAG_End.to_stream(stream)


class IntArrayTag(Tag):
    def _parse_impl(self, stream):
        element_type = TAG_Int
        length = self._parse_length(TAG_Int, stream)

        return [element_type._parse_impl(stream) for i in compat.range(length)]

    def _dump_impl(self, data, stream):
        self._dump_length(TAG_Int, len(data), stream)
        for elem in data:
            TAG_Int._dump_impl(elem, stream)


class LongArrayTag(Tag):
    def _parse_impl(self, stream):
        element_type = TAG_Long
        length = self._parse_length(TAG_Long, stream)

        return [element_type._parse_impl(stream) for i in compat.range(length)]

    def _dump_impl(self, data, stream):
        self._dump_length(TAG_Long, len(data), stream)
        for elem in data:
            TAG_Long._dump_impl(elem, stream)


TAG_End = EndTag("end", 0)
TAG_Byte = FixedTag("byte", 1, 1, "b")
TAG_Short = FixedTag("short", 2, 2, "h")
TAG_Int = FixedTag("int", 3, 4, "i")
TAG_Long = FixedTag("long", 4, 8, "q")
TAG_Float = FixedTag("float", 5, 4, "f")
TAG_Double = FixedTag("double", 6, 8, "d")
TAG_Byte_Array = VariableTag("byte_array", 7, TAG_Int)
TAG_String = VariableTag("string", 8, TAG_Short, encoding="utf-8")
TAG_List = ListTag("list", 9)
TAG_Compound = CompoundTag("compound", 10)
TAG_Int_Array = IntArrayTag("int_array", 11)
TAG_Long_Array = LongArrayTag("long_array", 12)


def parse_nbt(stream, gzipped=True):
    """Parse an .nbt file from the given stream.

    :param stream: a file-like stream configured for read().
    :param gzipped: if True, assume the stream is in gzip format first.
    :return: a Python structure representing the .nbt file.

    """
    if gzipped:
        stream = gzip.GzipFile(fileobj=stream)
    type_ = Tag.from_stream(stream)
    return type_.parse(stream)


def dump_nbt(nbt, stream, gzipped=True):
    """Dump an .nbt structure generated by :func:`.parse_nbt`
    to the given stream.

    :param nbt: the structure returned by a :func:`.parse_nbt` call.
    :param stream: a file-like stream configured for write().
    :param gzipped: if True, pass the stream through gzip for final output.

    """
    if gzipped:
        stream = gzip.GzipFile(mode="wb", fileobj=stream)
    type_ = nbt[0]
    type_.dump(nbt, stream)
