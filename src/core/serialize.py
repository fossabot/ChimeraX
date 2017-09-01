# vim: set expandtab shiftwidth=4 softtabstop=4:

# === UCSF ChimeraX Copyright ===
# Copyright 2016 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  For details see:
# http://www.rbvi.ucsf.edu/chimerax/docs/licensing.html
# This notice must be embedded in or attached to all copies,
# including partial copies, of the software or any revisions
# or derivations thereof.
# === UCSF ChimeraX Copyright ===

"""
serialize: Support serialization of "simple" types
==================================================

Provide object serialization and deserialization for simple Python objects.
In this case, simple means numbers (int, float, numpy arrays), strings,
bytes, booleans, and non-recursive tuples, lists, sets, and dictionaries.
Recursive data-structures are not checked for and thus can cause an infinite
loop.  Arbitrary Python objects are not allowed.

Internally use pickle, with safeguards on what is written (so the author of
the code is more likely to find the bug before a user of the software does),
and on what is read.  The reading is more restrictive because the C-version
of the pickler will pickle objects, like arbtrary functions.  The
deserializer catches those mistakes, but later when the session is opened.

Version 1 of the protocol supports instances of the following types:

    :py:class:`bool`; :py:class:`int`; :py:class:`float`; :py:class:`complex`;
    numpy :py:class:`~numpy.ndarray`;
    :py:class:`str`; :py:class:`bytes`; :py:class:`bytearray`;
    type(:py:data:`None`);
    :py:class:`set`; :py:class:`frozenset`;
    :py:class:`dict`;
    :py:mod:`collections`' :py:class:`~collections.OrderedDict`,
    and :py:class:`~collections.deque`;
    :py:mod:`datetime`'s :py:class:`~datetime.datetime`,
    :py:class:`~datetime.timezone`; and :py:class:`~datetime.timedelta`;
    and :pillow:`PIL.Image.Image`.

"""
import msgpack
import pickle
import types  # for pickle support
# imports for supported "primitive" types and collections
# ** must be keep in sync with state.py **
import numpy
from collections import OrderedDict, deque
from datetime import datetime, timezone, timedelta
from PIL import Image
from .session import _UniqueName
from .state import FinalizedState

# TODO: remove pickle and msgpack v2 after corresponding sessions
# are no longer supported.
_PICKLE_PROTOCOL = 4


class _RestrictTable(dict):

    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        import copyreg
        if complex in copyreg.dispatch_table:
            self[complex] = copyreg.dispatch_table[complex]
        try:
            import numpy
            self[numpy.ndarray] = numpy.ndarray.__reduce__
        except ImportError:
            pass

    def get(self, cls, default=None):
        if isinstance(cls, types.BuiltinFunctionType):
            # need to allow for unpickling numpy arrays and other types
            return default
        if cls not in self:
            raise TypeError("Can not serialize class: %s" % cls.__name__)
        return dict.__getitem__(self, cls)


def pickle_serialize(stream, obj):
    """Put object in to a binary stream"""
    pickler = pickle.Pickler(stream, protocol=_PICKLE_PROTOCOL)
    pickler.fast = True     # no recursive lists/dicts/sets
    pickler.dispatch_table = _RestrictTable()
    pickler.dump(obj)


class _RestrictedUnpickler(pickle.Unpickler):

    supported = {
        'builtins': {'complex'},
        'collections': {'deque', 'Counter', 'OrderedDict'},
        'datetime': {'timedelta', 'timezone', 'datetime'},
        'numpy': {'ndarray', 'dtype'},
        'numpy.core.multiarray': {'_reconstruct', 'scalar'},
        'PIL.Image': {'Image'},
    }
    supported[_UniqueName.__module__] = {_UniqueName.__name__}
    supported[FinalizedState.__module__] = {FinalizedState.__name__}

    def find_class(self, module, name):
        if module in self.supported and name in self.supported[module]:
            return getattr(__import__(module, fromlist=(name,)), name)
        # Forbid everything else.
        fullname = '%s.%s' % (module, name)
        raise pickle.UnpicklingError("global '%s' is forbidden" % fullname)


def pickle_deserialize(stream):
    """Recover object from a binary stream"""
    unpickler = _RestrictedUnpickler(stream)
    return unpickler.load()


def _encode_image(img):
    import io
    stream = io.BytesIO()
    img.save(stream, format='PNG')
    data = stream.getvalue()
    stream.close()
    return data


def _decode_image(data):
    import io
    stream = io.BytesIO(data)
    img = Image.open(stream)
    img.load()
    return img


def _encode_ndarray_v2(o):
    # inspired by msgpack-numpy package
    if o.dtype.kind == 'V':
        # structured array
        kind = b'V'
        dtype = o.dtype.descr
    else:
        kind = b''
        dtype = o.dtype.str
    if 'O' in dtype:
        raise TypeError("Can not serialize numpy arrays of objects")
    return (
        (b'kind', kind), (b'dtype', dtype),
        (b'shape', o.shape), (b'data', o.tobytes())
    )


def _encode_ndarray(o):
    # inspired by msgpack-numpy package
    if o.dtype.kind == 'V':
        # structured array
        kind = b'V'
        dtype = o.dtype.descr
    else:
        kind = b''
        dtype = o.dtype.str
    if 'O' in dtype:
        raise TypeError("Can not serialize numpy arrays of objects")
    return {
        b'kind': kind,
        b'dtype': dtype,
        b'shape': list(o.shape),
        b'data': o.tobytes()
    }


def _decode_ndarray(data):
    kind = data[b'kind']
    dtype = data[b'dtype']
    if kind == b'V':
        dtype = [tuple(str(t) for t in d) for d in dtype]
    return numpy.fromstring(data[b'data'], numpy.dtype(dtype)).reshape(data[b'shape'])


def _encode_numpy_number_v2(o):
    return (
        (b'dtype', o.dtype.str), (b'data', o.tobytes())
    )


def _encode_numpy_number(o):
    return {
        b'dtype': o.dtype.str,
        b'data': o.tobytes()
    }


def _decode_numpy_number(data):
    return numpy.fromstring(data[b'data'], numpy.dtype(data[b'dtype']))[0]


def _decode_datetime(data):
    from dateutil.parser import parse
    return parse(data)


_encode_handlers_v2 = {
    # type : lambda returning OrderedDict with unique __type__ first
    # __type__ is index into decode array
    _UniqueName: lambda o: OrderedDict(
        (('__type__', 0), ('uid', o.uid))
    ),
    # __type__ == 1 is for numpy arrays
    complex: lambda o: OrderedDict(
        (('__type__', 2), ('args', (o.real, o.imag)))
    ),
    set: lambda o: OrderedDict(
        (('__type__', 3), ('args', tuple(o)))
    ),
    frozenset: lambda o: OrderedDict(
        (('__type__', 4), ('args', tuple(o)))
    ),
    OrderedDict: lambda o: OrderedDict(
        (('__type__', 5),) + tuple(o.items())
    ),
    deque: lambda o: OrderedDict(
        (('__type__', 6), ('args', tuple(o)))
    ),
    datetime: lambda o: OrderedDict(
        (('__type__', 7), ('arg', o.isoformat()))
    ),
    timedelta: lambda o: OrderedDict(
        (('__type__', 8), ('args', (o.days, o.seconds, o.microseconds)))
    ),
    Image.Image: lambda o: OrderedDict(
        (('__type__', 9), ('arg', _encode_image(o)))
    ),
    # __type__ == 10 is for numpy scalars
    FinalizedState: lambda o: OrderedDict(
        (('__type__', 11), ('arg', o.data))
    ),
    timezone: lambda o: OrderedDict(
        (('__type__', 12), ('arg', o.__getinitargs__()))
    ),
}


def _encode_v2(obj):
    cvt = _encode_handlers_v2.get(type(obj), None)
    if cvt is not None:
        return cvt(obj)
    # handle numpy subclasses
    if isinstance(obj, numpy.ndarray):
        return OrderedDict((('__type__', 1),) + _encode_ndarray_v2(obj))
    if isinstance(obj, (numpy.number, numpy.bool_, numpy.bool8)):
        return OrderedDict((('__type__', 10),) + _encode_numpy_number_v2(obj))

    obj_cls = type(obj)
    raise RuntimeError("Can't convert object of type: %s.%s" % (
                       obj_cls.__module__, obj_cls.__name__))


_decode_handlers_v2 = [
    # order must match encode's __type__ values
    lambda args: _UniqueName(args[0][1]),
    lambda args: _decode_ndarray(dict(args)),
    lambda args: complex(*args[0][1]),
    lambda args: set(args[0][1]),
    lambda args: frozenset(args[0][1]),
    OrderedDict,
    lambda args: deque(args[0][1]),
    lambda args: _decode_datetime(args[0][1]),
    lambda args: timedelta(*args[0][1]),
    lambda args: _decode_image(args[0][1]),
    lambda args: _decode_numpy_number(dict(args)),
    lambda args: FinalizedState(args[0][1]),
    lambda args: timezone(*args[0][1]),
]


def _decode_pairs_v2(pairs):
    try:
        len(pairs)
    except TypeError:
        pairs = tuple(pairs)
    if not pairs:
        return dict()
    if pairs[0][0] != '__type__':
        return OrderedDict(pairs)
    cvt = _decode_handlers_v2[pairs[0][1]]
    return cvt(pairs[1:])


def msgpack_serialize_stream_v2(stream):
    packer = msgpack.Packer(default=_encode_v2, use_bin_type=True,
                            use_single_float=False)
    return stream, packer


def msgpack_deserialize_stream_v2(stream):
    unpacker = msgpack.Unpacker(
        stream, object_pairs_hook=_decode_pairs_v2, encoding='utf-8',
        use_list=False)
    return unpacker


def _encode_unique_name(un):
    # Return byte representation for serialization
    import struct
    class_name, ordinal = un.uid
    try:
        bin_ord = struct.pack("<Q", ordinal)
        if ordinal < 2 ** 8:
            num_bytes = 1
        elif ordinal < 2 ** 16:
            num_bytes = 2
        elif ordinal < 2 ** 24:
            num_bytes = 3
        elif ordinal < 2 ** 32:
            num_bytes = 4
        elif ordinal < 2 ** 40:
            num_bytes = 5
        elif ordinal < 2 ** 48:
            num_bytes = 6
        elif ordinal < 2 ** 56:
            num_bytes = 7
        else:
            num_bytes = 8
        if isinstance(class_name, str):
            cn = bytes(class_name, 'utf-8')
            len_cn = len(cn)
            return struct.pack(
                "<BBB%ds%ds" % (len_cn, num_bytes),
                0, len_cn, num_bytes, cn, bin_ord)
        else:
            bn = bytes(class_name[0], 'utf-8')
            len_bn = len(bn)
            cn = bytes(class_name[1], 'utf-8')
            len_cn = len(cn)
            return struct.pack(
                "<BBBB%ds%ds%ds" % (len_bn, len_cn, num_bytes),
                1, len_bn, len_cn, num_bytes, bn, cn, bin_ord)
    except struct.error:
        # TODO: either string length > 255 or ordinal > 2^64-1
        raise RuntimeError("Unable to encode unique id")


def _decode_unique_name(buf):
    # restore _UniqueName from serialized representation
    import struct
    if buf[0] == 0:
        len_cn, num_bytes = struct.unpack("<BB", buf[1:3])
        class_name, ordinal = struct.unpack(
            "<%ds%ds" % (len_cn, num_bytes), buf[3:])
        class_name = class_name.decode()
    else:
        # assert buf[0] == 1
        len_bn, len_cn, num_bytes = struct.unpack("<BBB", buf[1:4])
        bundle_name, class_name, ordinal = struct.unpack(
            "<%ds%ds%ds" % (len_bn, len_cn, num_bytes), buf[4:])
        class_name = (bundle_name.decode(), class_name.decode())
    ordinal += (8 - num_bytes) * b'\0'
    ordinal, = struct.unpack("<Q", ordinal)
    uid = (class_name, ordinal)
    return _UniqueName(uid)


def _encode(obj):
    # Return msgpack extension type, limited to 0-127
    # In simple session test: # of tuples > # of UniqueNames > # of numpy arrays > the rest
    if isinstance(obj, tuple):
        # TODO: save as msgpack array without converting to list first
        # restored as a tuple
        return msgpack.ExtType(12, msgpack.packb(list(obj), **_packer_args))
    if isinstance(obj, _UniqueName):
        return msgpack.ExtType(0, _encode_unique_name(obj))
    if isinstance(obj, numpy.ndarray):
        # handle numpy array subclasses
        return msgpack.ExtType(1, msgpack.packb(_encode_ndarray(obj), **_packer_args))
    if isinstance(obj, complex):
        # restored as a tuple
        return msgpack.ExtType(2, msgpack.packb([obj.real, obj.imag], **_packer_args))
    if isinstance(obj, set):
        # TODO: save as msgpack array without converting to list first
        return msgpack.ExtType(3, msgpack.packb(list(obj), **_packer_args))
    if isinstance(obj, frozenset):
        # TODO: save as msgpack array without converting to list first
        return msgpack.ExtType(4, msgpack.packb(list(obj), **_packer_args))
    if isinstance(obj, OrderedDict):
        # TODO: save as msgpack array without converting to list first
        return msgpack.ExtType(5, msgpack.packb(list(obj.items()), **_packer_args))
    if isinstance(obj, deque):
        # TODO: save as msgpack array without converting to list first
        return msgpack.ExtType(6, msgpack.packb(list(obj), **_packer_args))
    if isinstance(obj, datetime):
        return msgpack.ExtType(7, msgpack.packb(obj.isoformat(), **_packer_args))
    if isinstance(obj, timedelta):
        # restored as a tuple
        return msgpack.ExtType(8, msgpack.packb([obj.days, obj.seconds, obj.microseconds], **_packer_args))
    if isinstance(obj, Image.Image):
        return msgpack.ExtType(9, _encode_image(obj))
    if isinstance(obj, (numpy.number, numpy.bool_, numpy.bool8)):
        # handle numpy scalar subclasses
        return msgpack.ExtType(10, msgpack.packb(_encode_numpy_number(obj), **_packer_args))
    if isinstance(obj, FinalizedState):
        return msgpack.ExtType(11, msgpack.packb(obj.data, **_packer_args))
    if isinstance(obj, timezone):
        # TODO: save as msgpack array without converting to list first
        # restored as a tuple
        return msgpack.ExtType(13, msgpack.packb(list(obj.__getinitargs__()), **_packer_args))

    raise RuntimeError("Can't convert object of type: %s" % type(obj))


_decode_handlers = (
    # order must match _encode ExtType's type code
    _decode_unique_name,
    lambda buf: _decode_ndarray(_decode_bytes(buf)),
    lambda buf: complex(*_decode_bytes_as_tuple(buf)),
    lambda buf: set(_decode_bytes(buf)),
    lambda buf: frozenset(_decode_bytes(buf)),
    lambda buf: OrderedDict(_decode_bytes(buf)),
    lambda buf: deque(_decode_bytes(buf)),
    lambda buf: _decode_datetime(_decode_bytes(buf)),
    lambda buf: timedelta(*_decode_bytes_as_tuple(buf)),
    lambda buf: _decode_image(buf),
    lambda buf: _decode_numpy_number(_decode_bytes(buf)),
    lambda buf: FinalizedState(_decode_bytes(buf)),
    lambda buf: _decode_bytes_as_tuple(buf),
    lambda buf: timezone(*_decode_bytes_as_tuple(buf)),
)
assert len(_decode_handlers) == 14


def _decode_bytes(buf):
    return msgpack.unpackb(buf, **_unpacker_args)


def _decode_bytes_as_tuple(buf):
    unpacker = msgpack.Unpacker(None, **_unpacker_args)
    unpacker.feed(buf)
    n = unpacker.read_array_header()

    def extract(unpacker=unpacker, n=n):
        for i in range(n):
            yield unpacker.unpack()
    return tuple(extract())


def _decode_ext(n, buf):
    # assert 0 <= n < len(_decode_handlers)
    return _decode_handlers[n](buf)


_packer_args = {
    'default': _encode,
    'encoding': 'utf-8',
    'use_bin_type': True,
    'use_single_float': False,
    'strict_types': True
}

_unpacker_args = {
    'ext_hook': _decode_ext,
    'encoding': 'utf-8'
}


def msgpack_serialize_stream(stream):
    packer = msgpack.Packer(**_packer_args)
    return stream, packer


def msgpack_deserialize_stream(stream):
    unpacker = msgpack.Unpacker(stream, **_unpacker_args)
    return unpacker


def msgpack_serialize(stream, obj):
    # _count_object_types(obj)  # DEBUG
    stream, packer = stream
    stream.write(packer.pack(obj))


def msgpack_deserialize(stream):
    try:
        return next(stream)
    except StopIteration:
        return None


# Debuging code for finding out object types used

_object_counts = {
    type(None): 0,
    bool: 0,
    int: 0,
    bytes: 0,
    bytearray: 0,
    str: 0,
    memoryview: 0,
    float: 0,
    list: 0,
    dict: 0,

    # extension types
    _UniqueName: 0,
    numpy.ndarray: 0,
    complex: 0,
    set: 0,
    frozenset: 0,
    OrderedDict: 0,
    deque: 0,
    datetime: 0,
    timedelta: 0,
    Image.Image: 0,
    numpy.number: 0,
    FinalizedState: 0,
    tuple: 0,
    timezone: 0,
}

_extention_types = [
    _UniqueName,
    numpy.ndarray,
    complex,
    set,
    frozenset,
    OrderedDict,
    deque,
    datetime,
    timedelta,
    Image.Image,
    numpy.number,
    FinalizedState,
    tuple,
    timezone,
]


def _reset_object_counts():
    for t in _object_counts:
        _object_counts[t] = 0


def _count_object_types(obj):
    # handle numpy subclasses
    if isinstance(obj, numpy.ndarray):
        _object_counts[numpy.ndarray] += 1
        return
    if isinstance(obj, (numpy.number, numpy.bool_, numpy.bool8)):
        _object_counts[numpy.number] += 1
        return
    t = type(obj)
    _object_counts[t] += 1
    if t == FinalizedState:
        _count_object_types(obj.data)
        return
    if t in (list, tuple, set, frozenset, deque):
        for o in obj:
            _count_object_types(o)
        return
    if t in (dict, OrderedDict):
        for k, v in obj.items():
            _count_object_types(k)
            _count_object_types(v)
        return


def _print_object_counts():
    types = list(_object_counts)
    # types = list(_extention_types)
    types.sort(key=lambda t: t.__name__)
    for t in types:
        print('%s: %s' % (t.__name__, _object_counts[t]))


if __name__ == '__main__':
    import io

    def serialize(buf, obj):
        # packer = msgpack_serialize_stream_v2(buf)
        packer = msgpack_serialize_stream(buf)
        msgpack_serialize(packer, obj)

    def deserialize(buf):
        # unpacker = msgpack_deserialize_stream_v2(buf)
        unpacker = msgpack_deserialize_stream(buf)
        return msgpack_deserialize(unpacker)

    # serialize = pickle_serialize
    # deserialize = pickle_deserialize

    def test(obj, msg, expect_pass=True, idempotent=True):
        passed = 'pass' if expect_pass else 'fail'
        failed = 'fail' if expect_pass else 'pass'
        with io.BytesIO() as buf:
            try:
                serialize(buf, obj)
            except Exception as e:
                if failed == "fail":
                    print('%s (serialize): %s: %s' % (failed, msg, e))
                else:
                    print('%s (serialize): %s' % (failed, msg))
                return
            buf.seek(0)
            try:
                result = deserialize(buf)
            except Exception as e:
                if failed == "fail":
                    print('%s (deserialize): %s: %s' % (failed, msg, e))
                else:
                    print('%s (deserialize): %s' % (failed, msg))
                return
            try:
                if isinstance(obj, numpy.ndarray):
                    assert(numpy.array_equal(result, obj))
                else:
                    assert(result == obj)
            except AssertionError:
                if idempotent:
                    print('%s: %s: not idempotent' % (failed, msg))
                    print('  original:', obj)
                    print('  result:', result)
                else:
                    print('%s: %s' % (passed, msg))
            else:
                print('%s: %s' % (passed, msg))

    # test: basic type support
    test(3, 'an int')
    test(42.0, 'a float')
    test('chimera', 'a string')
    test(complex(3, 4), 'a complex')
    test(False, 'False')
    test(True, 'True')
    test(None, 'None')
    test(b'xyzzy', 'some bytes')
    test(((0, 1), (2, 0)), 'nested tuples')
    test([[0, 1], [2, 0]], 'nested lists')
    test({'a': {0: 1}, 'b': {2: 0}}, 'nested dicts')
    test({1, 2, frozenset([3, 4])}, 'frozenset nested in a set')
    test(bool, 'can not serialize bool', expect_pass=False)
    test(float, 'can not serialize float', expect_pass=False)
    test(int, 'can not serialize int', expect_pass=False)
    test(set, 'can not serialize set', expect_pass=False)

    # test: objects
    class C:
        pass
    test_obj = C()
    test_obj.test = 12
    test(C, 'can not serialize class definition', expect_pass=False)
    test(test_obj, 'can not serialize objects', expect_pass=False)

    # test: functions
    test(serialize, 'can not serialize function objects', expect_pass=False)
    test(abs, 'can not serialize builtin functions', expect_pass=False)

    # test: numpy arrays
    test_obj = numpy.zeros((2, 2), dtype=numpy.float32)
    test(test_obj, 'numerical numpy array')
    test_obj = numpy.empty((2, 2), dtype=numpy.float32)
    test(test_obj, 'empty numerical numpy array')

    class C:
        pass
    test_obj = numpy.empty((2, 2), dtype=object)
    test_obj[:, :] = C()
    test(test_obj, 'can not serialize numpy array of objects',
         expect_pass=False)
    test_obj = numpy.float32(3.14159)
    test(test_obj, 'numpy float32 number')

    import sys
    if sys.platform.startswith('win'):
        with open("nul:") as f:
            test(f, 'can not serialize file object', expect_pass=False)
    else:
        with open("/bin/ls") as f:
            test(f, 'can not serialize file object', expect_pass=False)

    # d = date(2000, 1, 1)
    # test(d, 'date')
    # t = time()
    # test(t, 'time')
    t = timedelta()
    test(t, 'timedelta')
    d = datetime.now()
    test(d, 'datetime')
    d = datetime.now().astimezone()
    test(d, 'datetime&timezone')
    d = datetime.now(timezone.utc)
    test(d, 'datetime&utc timezone')
    test(timezone.utc, 'utc timezone')

    import enum

    class Color(enum.Enum):
        red = 1
    c = Color.red
    test(c, 'can not serialize Enum subclass', expect_pass=False)

    class Color(enum.IntEnum):
        red = 1
    c = Color.red
    test(c, 'IntEnum subclass instance', expect_pass=False)

    d = OrderedDict([(1, 2), (3, 4), (5, 6), (7, 8)])
    test(d, 'ordered dict')

    test(Image.new("RGB", (32, 32), "white"), 'PIL image', idempotent=False)

    test(_UniqueName((('module', 'class'), 10)), 'UniqueName')
