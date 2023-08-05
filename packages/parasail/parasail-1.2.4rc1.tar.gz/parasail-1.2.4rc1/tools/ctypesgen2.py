#!/usr/bin/env python

# Creates the parasail/bindings_v2.py file used for the python bindings.

import sys

def myprint(arg):
    sys.stdout.write(arg+"\n")

myprint("""
import ctypes
import platform
import os
import re
import sys

import numpy

_libname = "libparasail.so"
if platform.system() == 'Darwin':
    _libname = "libparasail.dylib"
elif platform.system() == 'Windows':
    _libname = "parasail.dll"
_libpath = os.path.join(os.path.dirname(__file__), _libname)

_verbose = os.environ.get("PARASAIL_VERBOSE", False)

# attempt to load library from package location
_lib = None
try:
    _lib = ctypes.CDLL(_libpath)
except:
    if _verbose: print("failed to open '{}' in package location".format(_libname))

if not _lib:
    try:
        _lib = ctypes.CDLL(_libname)
    except:
        if _verbose: print("failed to open '{}' using ctypes.CDLL defaults".format(_libname))

def _lib_search():
    global _lib
    global _libpath
    _libpath = None
    for env_var in ["PARASAIL_LIBPATH", "LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH", "PATH"]:
        if env_var in os.environ:
            if _verbose: print("searching {} for {}".format(env_var,_libname))
            for path in re.split("[:;]", os.environ[env_var]):
                if _verbose: print("searching {}".format(path))
                for attempt in [os.path.join(root,_libname) for root,dirs,files in os.walk(path) if _libname in files]:
                    try:
                        _lib = ctypes.CDLL(attempt)
                        _libpath = attempt
                        if _verbose: print("found '{}'".format(attempt))
                        return
                    except:
                        if _verbose: print("attempted but failed to load '{}'".format(attempt))
        else:
            if _verbose: print("env var {} not set".format(env_var))

# if library load failed, search for it
if not _lib:
    _lib_search()

# library load still failed, hard error
if not _lib:
    raise Exception("failed to locate and open '{}'".format(_libname))

_case_sensitive = False
def set_case_sensitive(case):
    global _case_sensitive
    _case_sensitive = case

_alphabet_aliases = None
def set_alphabet_aliases(alias):
    global _alphabet_aliases
    _alphabet_aliases = alias

_encoding = 'latin_1'
def set_encoding(encoding):
    global _encoding
    try:
        (' '.encode(encoding)).decode(encoding)
    except LookupError:
        raise Exception("Encoding '{}' not supported".format(encoding))
    _encoding = encoding

if sys.version_info.major < 3:
    def b(x):
        if x is None:
            return None
        else:
            return str(x)
    def s(x):
        return str(x)
    def isstr(s):
        return isinstance(s, basestring)
else:
    def isstr(s):
        return isinstance(s, str)
    def isbytes(s):
        return isinstance(s, (bytes, bytearray))
    def b(x):
        if isstr(x):
            return x.encode(_encoding)
        else:
            return x
    def s(x):
        if isbytes(x):
            return x.decode(_encoding)
        else:
            return x

def _make_nd_array(c_pointer, shape, dtype=numpy.intc, order='C', own_data=True):
    arr_size = numpy.prod(shape[:]) * numpy.dtype(dtype).itemsize
    if sys.version_info.major >= 3:
        buf_from_mem = ctypes.pythonapi.PyMemoryView_FromMemory
        buf_from_mem.restype = ctypes.py_object
        buf_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_int)
        buffer = buf_from_mem(c_pointer, arr_size, 0x100)
    else:
        buf_from_mem = ctypes.pythonapi.PyBuffer_FromMemory
        buf_from_mem.restype = ctypes.py_object
        buf_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_ssize_t)
        buffer = buf_from_mem(c_pointer, arr_size)
    return numpy.ndarray(tuple(shape[:]), dtype, buffer, order=order)

c_int_p = ctypes.POINTER(ctypes.c_int)

class result_t(ctypes.Structure):
    _fields_ = [
       ("score",         ctypes.c_int),
       ("end_query",     ctypes.c_int),
       ("end_ref",       ctypes.c_int),
       ("flag",          ctypes.c_int),
       ("extra",         ctypes.c_void_p)
       ]

c_result_p = ctypes.POINTER(result_t)

c_uint32_p = ctypes.POINTER(ctypes.c_uint32)

class traceback_t(ctypes.Structure):
    _fields_ = [
        ("query", ctypes.c_char_p),
        ("comp",  ctypes.c_char_p),
        ("ref",   ctypes.c_char_p)
    ]

c_traceback_p = ctypes.POINTER(traceback_t)

class cigar_t(ctypes.Structure):
    _fields_ = [
        ("seq",       c_uint32_p),
        ("len",       ctypes.c_int),
        ("beg_query", ctypes.c_int),
        ("beg_ref",   ctypes.c_int)
    ]

c_cigar_p = ctypes.POINTER(cigar_t)

class result_ssw_t(ctypes.Structure):
    _fields_ = [
        ("score1",      ctypes.c_uint16),
        ("ref_begin1",  ctypes.c_int32),
        ("ref_end1",    ctypes.c_int32),
        ("read_begin1", ctypes.c_int32),
        ("read_end1",   ctypes.c_int32),
        ("cigar",       c_uint32_p),
        ("cigarLen",    ctypes.c_int32)
    ]

c_result_ssw_p = ctypes.POINTER(result_ssw_t)

class pstring_t(ctypes.Structure):
    _fields_ = [
        ("l", ctypes.c_size_t),
        ("s", ctypes.c_char_p)
    ]

class sequence_t(ctypes.Structure):
    _fields_ = [
        ("name",    pstring_t),
        ("comment", pstring_t),
        ("seq",     pstring_t),
        ("qual",    pstring_t)
    ]

c_sequence_p = ctypes.POINTER(sequence_t)

class sequences_t(ctypes.Structure):
    _fields_ = [
        ("seqs",       c_sequence_p),
        ("l",          ctypes.c_size_t),
        ("characters", ctypes.c_size_t),
        ("shortest",   ctypes.c_size_t),
        ("longest",    ctypes.c_size_t),
        ("mean",       ctypes.c_float),
        ("stddev",     ctypes.c_float)
    ]

c_sequences_p = ctypes.POINTER(sequences_t)

class Traceback:
    def __init__(self, pointer):
        self.pointer = pointer
    def __del__(self):
        if _lib:
            _lib.parasail_traceback_free(self.pointer)
    @property
    def query(self):
        return s(self.pointer[0].query)
    @property
    def comp(self):
        return s(self.pointer[0].comp)
    @property
    def ref(self):
        return s(self.pointer[0].ref)

class Cigar:
    __BAM_CIGAR_STR = 'MIDNSHP=X8'
    def __init__(self, pointer):
        self.pointer = pointer
    def __del__(self):
        if _lib:
            _lib.parasail_cigar_free(self.pointer)
    @property
    def seq(self):
        return _make_nd_array(
            self.pointer[0].seq,
            (self.pointer[0].len,),
            numpy.uint32)
    @property
    def len(self):
        return self.pointer[0].len
    @property
    def beg_query(self):
        return self.pointer[0].beg_query
    @property
    def beg_ref(self):
        return self.pointer[0].beg_ref
    @property
    def decode(self):
        # The C interface allocates unaligned memory but does not provide a
        # means of deallocating it.  The parasail_free() is for aligned
        # memory only.  On Windows, this is an error.  On OSX/Linux, free()
        # is the same for aligned and unaligned.
        if platform.system() == 'Windows':
            def _decode(x):
                l = str(x>>4)
                try:
                    c = self.__BAM_CIGAR_STR[x&0xf]
                except:
                    c = 'M'
                return l+c
            return ''.join([_decode(self.pointer[0].seq[i]) for i in range(self.pointer[0].len)])
        else:
            # this allocates a char array, and we must free it
            voidp = _lib.parasail_cigar_decode(self.pointer)
            as_str = ctypes.string_at(voidp)
            _lib.parasail_free(voidp)
            return as_str
    @staticmethod
    def decode_op(cigar_int):
        return _lib.parasail_cigar_decode_op(cigar_int)
    @staticmethod
    def decode_len(cigar_int):
        return _lib.parasail_cigar_decode_len(cigar_int)

class Result:
    def __init__(self, pointer, len_query, len_ref, query=None, ref=None, matrix=None):
        self.pointer = pointer
        self.len_query = len_query
        self.len_ref = len_ref
        self.query = query
        self.ref = ref
        self.matrix = matrix
        self._as_parameter_ = pointer
        self._cigar = None
        self._traceback = None
        self._traceback_args = None
    def __del__(self):
        if _lib:
            _lib.parasail_result_free(self.pointer)
    @property
    def saturated(self):
        return _lib.parasail_result_is_saturated(self.pointer) != 0
    @property
    def score(self):
        return self.pointer[0].score
    @property
    def matches(self):
        if 0 == _lib.parasail_result_is_stats(self.pointer):
            raise AttributeError("'Result' object has no stats")
        return _lib.parasail_result_get_matches(self.pointer)
    @property
    def similar(self):
        if 0 == _lib.parasail_result_is_stats(self.pointer):
            raise AttributeError("'Result' object has no stats")
        return _lib.parasail_result_get_similar(self.pointer)
    @property
    def length(self):
        if 0 == _lib.parasail_result_is_stats(self.pointer):
            raise AttributeError("'Result' object has no stats")
        return _lib.parasail_result_get_length(self.pointer)
    @property
    def end_query(self):
        return self.pointer[0].end_query
    @property
    def end_ref(self):
        return self.pointer[0].end_ref
    @property
    def score_table(self):
        if (0 == _lib.parasail_result_is_table(self.pointer) and
            0 == _lib.parasail_result_is_stats_table(self.pointer)):
            raise AttributeError("'Result' object has no score table")
        return _make_nd_array(
            _lib.parasail_result_get_score_table(self.pointer),
            (self.len_query, self.len_ref))
    @property
    def matches_table(self):
        if 0 == _lib.parasail_result_is_stats_table(self.pointer):
            raise AttributeError("'Result' object has no stats tables")
        return _make_nd_array(
            _lib.parasail_result_get_matches_table(self.pointer),
            (self.len_query, self.len_ref))
    @property
    def similar_table(self):
        if 0 == _lib.parasail_result_is_stats_table(self.pointer):
            raise AttributeError("'Result' object has no stats tables")
        return _make_nd_array(
            _lib.parasail_result_get_similar_table(self.pointer),
            (self.len_query, self.len_ref))
    @property
    def length_table(self):
        if 0 == _lib.parasail_result_is_stats_table(self.pointer):
            raise AttributeError("'Result' object has no stats tables")
        return _make_nd_array(
            _lib.parasail_result_get_length_table(self.pointer),
            (self.len_query, self.len_ref))
    @property
    def score_row(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_score_row(self.pointer),
            (self.len_ref,))
    @property
    def matches_row(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_matches_row(self.pointer),
            (self.len_ref,))
    @property
    def similar_row(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_similar_row(self.pointer),
            (self.len_ref,))
    @property
    def length_row(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_length_row(self.pointer),
            (self.len_ref,))
    @property
    def score_col(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_score_col(self.pointer),
            (self.len_query,))
    @property
    def matches_col(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_matches_col(self.pointer),
            (self.len_query,))
    @property
    def similar_col(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_similar_col(self.pointer),
            (self.len_query,))
    @property
    def length_col(self):
        if 0 == _lib.parasail_result_is_rowcol(self.pointer):
            raise AttributeError("'Result' object has no row/col arrays")
        return _make_nd_array(
            _lib.parasail_result_get_length_col(self.pointer),
            (self.len_query,))
    def get_cigar(self, case_sensitive=None, alphabet_aliases=None):
        if 0 == _lib.parasail_result_is_trace(self.pointer):
            raise AttributeError("'Result' object has no traceback")
        case = case_sensitive or _case_sensitive
        alias = alphabet_aliases or _alphabet_aliases
        if self._cigar is None:
            self._cigar = Cigar(_lib.parasail_result_get_cigar_extra(
                self.pointer,
                b(self.query), self.len_query,
                b(self.ref), self.len_ref,
                self.matrix,
                case, b(alias)))
        return self._cigar
    @property
    def cigar(self):
        return self.get_cigar()
    def get_traceback(self, mch='|', sim=':', neg='.', case_sensitive=None, alphabet_aliases=None):
        if 0 == _lib.parasail_result_is_trace(self.pointer):
            raise AttributeError("'Result' object has no traceback")
        case = case_sensitive or _case_sensitive
        alias = alphabet_aliases or _alphabet_aliases
        args = ''.join([mch,sim,neg,str(case),str(alias)])
        if self._traceback is None or self._traceback_args != args:
            self._traceback_args = args
            self._traceback = Traceback(_lib.parasail_result_get_traceback_extra(
                self.pointer,
                b(self.query), self.len_query,
                b(self.ref), self.len_ref,
                self.matrix,
                b(mch)[0], b(sim)[0], b(neg)[0],
                case, b(alias)))
        return self._traceback
    @property
    def traceback(self):
        return self.get_traceback()

class matrix_t(ctypes.Structure):
    _fields_ = [
        ("name",        ctypes.c_char_p),
        ("matrix",      c_int_p),
        ("mapper",      c_int_p),
        ("size",        ctypes.c_int),
        ("max",         ctypes.c_int),
        ("min",         ctypes.c_int),
        ("user_matrix", c_int_p)
        ]

c_matrix_p = ctypes.POINTER(matrix_t)

class Matrix:
    def __init__(self, pointer_or_string, case_sensitive=None):
        pointer = None
        if isstr(pointer_or_string):
            pointer = _lib.parasail_matrix_lookup(b(pointer_or_string))
            if not pointer:
                case = case_sensitive or _case_sensitive
                # matrix_from_file calls exit if file doesn't exist
                # so check now to avoid python exiting
                if os.path.isfile(pointer_or_string):
                    if case:
                        pointer = _lib.parasail_matrix_from_file_case_sensitive(
                                b(pointer_or_string))
                    else:
                        pointer = _lib.parasail_matrix_from_file(
                                b(pointer_or_string))
                else:
                    raise ValueError("Cannot open matrix file `%s'"%
                            pointer_or_string)
                if not pointer:
                    raise ValueError('specified matrix not found')
        else:
            pointer = pointer_or_string
        self.pointer = pointer
        self._as_parameter_ = pointer
    def __del__(self):
        if self.pointer[0].user_matrix and _lib:
            _lib.parasail_matrix_free(self.pointer)
    @property
    def name(self):
        return self.pointer[0].name
    @property
    def matrix(self):
        return _make_nd_array(
            self.pointer[0].matrix,
            (self.pointer[0].size, self.pointer[0].size))
    @property
    def mapper(self):
        return _make_nd_array( self.pointer[0].mapper, (256,))
    @property
    def size(self):
        return self.pointer[0].size
    @property
    def max(self):
        return self.pointer[0].max
    @property
    def min(self):
        return self.pointer[0].min
    def set_value(self, row, col, value):
        _lib.parasail_matrix_set_value(self.pointer, row, col, value)
    def copy(self):
        return Matrix(_lib.parasail_matrix_copy(self.pointer))
    def __setitem__(self, key, value):
        if type(key) is list or type(key) is tuple:
            if len(key) < 2:
                raise IndexError('too few keys in setitem')
            if len(key) > 2:
                raise IndexError('too many keys in setitem')
            if isinstance(key[0], slice) and isinstance(key[1], slice):
                for r in range(key[0].start, key[0].stop, key[0].step or 1):
                    for c in range(key[1].start, key[1].stop, key[1].step or 1):
                        _lib.parasail_matrix_set_value(self.pointer, r, c, value)
            elif isinstance(key[0], slice):
                for r in range(key[0].start, key[0].stop, key[0].step or 1):
                    _lib.parasail_matrix_set_value(self.pointer, r, key[1], value)

            elif isinstance(key[1], slice):
                for c in range(key[1].start, key[1].stop, key[1].step or 1):
                    _lib.parasail_matrix_set_value(self.pointer, key[0], c, value)
            else:
                _lib.parasail_matrix_set_value(self.pointer, key[0], key[1], value)
        elif isinstance(key, slice):
            for r in range(key[0].start, key[0].stop, key[0].step or 1):
                for c in range(self.size):
                    _lib.parasail_matrix_set_value(self.pointer, r, c, value)
        else:
            # assume int, do what numpy does
            for c in range(self.size):
                _lib.parasail_matrix_set_value(self.pointer, key, c, value)

class profile_data_t(ctypes.Structure):
    _fields_ = [
        ("score", ctypes.c_void_p),
        ("matches", ctypes.c_void_p),
        ("similar", ctypes.c_void_p)
    ]

class profile_t(ctypes.Structure):
    _fields_ = [
        ("s1", ctypes.c_char_p),
        ("s1Len", ctypes.c_int),
        ("matrix", c_matrix_p),
        ("profile8", profile_data_t),
        ("profile16", profile_data_t),
        ("profile32", profile_data_t),
        ("profile64", profile_data_t),
        ("free", ctypes.c_void_p),
        ("stop", ctypes.c_int)
        ]

c_profile_p = ctypes.POINTER(profile_t)

class Profile:
    def __init__(self, pointer, matrix, s1b):
        self.pointer = pointer
        self.matrix_ = matrix
        self._as_parameter_ = pointer
        self.s1b = s1b
    def __del__(self):
        if _lib:
            _lib.parasail_profile_free(self.pointer)
    @property
    def s1(self):
        return s(self.pointer[0].s1)
    @property
    def s1Len(self):
        return self.pointer[0].s1Len
    @property
    def matrix(self):
        return self.matrix_

_profile_create_argtypes = [ctypes.c_char_p, ctypes.c_int, c_matrix_p]

_lib.parasail_profile_create_8.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_8.restype = c_profile_p

_lib.parasail_profile_create_16.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_16.restype = c_profile_p

_lib.parasail_profile_create_32.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_32.restype = c_profile_p

_lib.parasail_profile_create_64.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_64.restype = c_profile_p

_lib.parasail_profile_create_sat.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_sat.restype = c_profile_p

_lib.parasail_profile_create_stats_8.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_8.restype = c_profile_p

_lib.parasail_profile_create_stats_16.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_16.restype = c_profile_p

_lib.parasail_profile_create_stats_32.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_32.restype = c_profile_p

_lib.parasail_profile_create_stats_64.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_64.restype = c_profile_p

_lib.parasail_profile_create_stats_sat.argtypes = _profile_create_argtypes
_lib.parasail_profile_create_stats_sat.restype = c_profile_p

def profile_create_8(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_8(s1b, len(s1), matrix), matrix, s1b)

def profile_create_16(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_16(s1b, len(s1), matrix), matrix, s1b)

def profile_create_32(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_32(s1b, len(s1), matrix), matrix, s1b)

def profile_create_64(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_64(s1b, len(s1), matrix), matrix, s1b)

def profile_create_sat(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_sat(s1b, len(s1), matrix), matrix, s1b)

def profile_create_stats_8(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_stats_8(s1b, len(s1), matrix), matrix, s1b)

def profile_create_stats_16(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_stats_16(s1b, len(s1), matrix), matrix, s1b)

def profile_create_stats_32(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_stats_32(s1b, len(s1), matrix), matrix, s1b)

def profile_create_stats_64(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_stats_64(s1b, len(s1), matrix), matrix, s1b)

def profile_create_stats_sat(s1, matrix):
    s1b = b(s1)
    return Profile(_lib.parasail_profile_create_stats_sat(s1b, len(s1), matrix), matrix, s1b)

def can_use_avx2():
    return bool(_lib.parasail_can_use_avx2())

def can_use_sse41():
    return bool(_lib.parasail_can_use_sse41())

def can_use_sse2():
    return bool(_lib.parasail_can_use_sse2())

def can_use_altivec():
    return bool(_lib.parasail_can_use_altivec())

def can_use_neon():
    return bool(_lib.parasail_can_use_neon())

# begin non-alignment functions defined here

_lib.parasail_free.argtypes = [ctypes.c_void_p]
_lib.parasail_free.restype = None

# parasail_profile_free is not exposed.
# Memory is managed by the Profile class.
_lib.parasail_profile_free.argtypes = [c_profile_p]
_lib.parasail_profile_free.restype = None

# parasail_result_free is not exposed.
# Memory is managed by the Result class.
_lib.parasail_result_free.argtypes = [c_result_p]
_lib.parasail_result_free.restype = None

_lib.parasail_time.argtypes = []
_lib.parasail_time.restype = ctypes.c_double

def time():
    return _lib.parasail_time()

_lib.parasail_matrix_lookup
_lib.parasail_matrix_lookup.argtypes = [ctypes.c_char_p]
_lib.parasail_matrix_lookup.restype = c_matrix_p

_lib.parasail_matrix_from_file
_lib.parasail_matrix_from_file.argtypes = [ctypes.c_char_p]
_lib.parasail_matrix_from_file.restype = c_matrix_p

_lib.parasail_matrix_from_file_case_sensitive
_lib.parasail_matrix_from_file_case_sensitive.argtypes = [ctypes.c_char_p]
_lib.parasail_matrix_from_file_case_sensitive.restype = c_matrix_p

blosum100 = Matrix(_lib.parasail_matrix_lookup(b("blosum100")))
blosum30 = Matrix(_lib.parasail_matrix_lookup(b("blosum30")))
blosum35 = Matrix(_lib.parasail_matrix_lookup(b("blosum35")))
blosum40 = Matrix(_lib.parasail_matrix_lookup(b("blosum40")))
blosum45 = Matrix(_lib.parasail_matrix_lookup(b("blosum45")))
blosum50 = Matrix(_lib.parasail_matrix_lookup(b("blosum50")))
blosum55 = Matrix(_lib.parasail_matrix_lookup(b("blosum55")))
blosum60 = Matrix(_lib.parasail_matrix_lookup(b("blosum60")))
blosum62 = Matrix(_lib.parasail_matrix_lookup(b("blosum62")))
blosum65 = Matrix(_lib.parasail_matrix_lookup(b("blosum65")))
blosum70 = Matrix(_lib.parasail_matrix_lookup(b("blosum70")))
blosum75 = Matrix(_lib.parasail_matrix_lookup(b("blosum75")))
blosum80 = Matrix(_lib.parasail_matrix_lookup(b("blosum80")))
blosum85 = Matrix(_lib.parasail_matrix_lookup(b("blosum85")))
blosum90 = Matrix(_lib.parasail_matrix_lookup(b("blosum90")))
pam10 = Matrix(_lib.parasail_matrix_lookup(b("pam10")))
pam100 = Matrix(_lib.parasail_matrix_lookup(b("pam100")))
pam110 = Matrix(_lib.parasail_matrix_lookup(b("pam110")))
pam120 = Matrix(_lib.parasail_matrix_lookup(b("pam120")))
pam130 = Matrix(_lib.parasail_matrix_lookup(b("pam130")))
pam140 = Matrix(_lib.parasail_matrix_lookup(b("pam140")))
pam150 = Matrix(_lib.parasail_matrix_lookup(b("pam150")))
pam160 = Matrix(_lib.parasail_matrix_lookup(b("pam160")))
pam170 = Matrix(_lib.parasail_matrix_lookup(b("pam170")))
pam180 = Matrix(_lib.parasail_matrix_lookup(b("pam180")))
pam190 = Matrix(_lib.parasail_matrix_lookup(b("pam190")))
pam20 = Matrix(_lib.parasail_matrix_lookup(b("pam20")))
pam200 = Matrix(_lib.parasail_matrix_lookup(b("pam200")))
pam210 = Matrix(_lib.parasail_matrix_lookup(b("pam210")))
pam220 = Matrix(_lib.parasail_matrix_lookup(b("pam220")))
pam230 = Matrix(_lib.parasail_matrix_lookup(b("pam230")))
pam240 = Matrix(_lib.parasail_matrix_lookup(b("pam240")))
pam250 = Matrix(_lib.parasail_matrix_lookup(b("pam250")))
pam260 = Matrix(_lib.parasail_matrix_lookup(b("pam260")))
pam270 = Matrix(_lib.parasail_matrix_lookup(b("pam270")))
pam280 = Matrix(_lib.parasail_matrix_lookup(b("pam280")))
pam290 = Matrix(_lib.parasail_matrix_lookup(b("pam290")))
pam30 = Matrix(_lib.parasail_matrix_lookup(b("pam30")))
pam300 = Matrix(_lib.parasail_matrix_lookup(b("pam300")))
pam310 = Matrix(_lib.parasail_matrix_lookup(b("pam310")))
pam320 = Matrix(_lib.parasail_matrix_lookup(b("pam320")))
pam330 = Matrix(_lib.parasail_matrix_lookup(b("pam330")))
pam340 = Matrix(_lib.parasail_matrix_lookup(b("pam340")))
pam350 = Matrix(_lib.parasail_matrix_lookup(b("pam350")))
pam360 = Matrix(_lib.parasail_matrix_lookup(b("pam360")))
pam370 = Matrix(_lib.parasail_matrix_lookup(b("pam370")))
pam380 = Matrix(_lib.parasail_matrix_lookup(b("pam380")))
pam390 = Matrix(_lib.parasail_matrix_lookup(b("pam390")))
pam40 = Matrix(_lib.parasail_matrix_lookup(b("pam40")))
pam400 = Matrix(_lib.parasail_matrix_lookup(b("pam400")))
pam410 = Matrix(_lib.parasail_matrix_lookup(b("pam410")))
pam420 = Matrix(_lib.parasail_matrix_lookup(b("pam420")))
pam430 = Matrix(_lib.parasail_matrix_lookup(b("pam430")))
pam440 = Matrix(_lib.parasail_matrix_lookup(b("pam440")))
pam450 = Matrix(_lib.parasail_matrix_lookup(b("pam450")))
pam460 = Matrix(_lib.parasail_matrix_lookup(b("pam460")))
pam470 = Matrix(_lib.parasail_matrix_lookup(b("pam470")))
pam480 = Matrix(_lib.parasail_matrix_lookup(b("pam480")))
pam490 = Matrix(_lib.parasail_matrix_lookup(b("pam490")))
pam50 = Matrix(_lib.parasail_matrix_lookup(b("pam50")))
pam500 = Matrix(_lib.parasail_matrix_lookup(b("pam500")))
pam60 = Matrix(_lib.parasail_matrix_lookup(b("pam60")))
pam70 = Matrix(_lib.parasail_matrix_lookup(b("pam70")))
pam80 = Matrix(_lib.parasail_matrix_lookup(b("pam80")))
pam90 = Matrix(_lib.parasail_matrix_lookup(b("pam90")))
dnafull = Matrix(_lib.parasail_matrix_lookup(b("dnafull")))
nuc44 = Matrix(_lib.parasail_matrix_lookup(b("nuc44")))

_lib.parasail_matrix_create.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_lib.parasail_matrix_create.restype = c_matrix_p

_lib.parasail_matrix_create_case_sensitive.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_lib.parasail_matrix_create_case_sensitive.restype = c_matrix_p

def matrix_create(alphabet, match, mismatch, case_sensitive=None):
    case = case_sensitive or _case_sensitive
    if case:
        return Matrix(_lib.parasail_matrix_create_case_sensitive(b(alphabet), match, mismatch))
    else:
        return Matrix(_lib.parasail_matrix_create(b(alphabet), match, mismatch))

# parasail_matrix_free is not exposed.
# Memory is managed by the Matrix class.
_lib.parasail_matrix_free.argtypes = [c_matrix_p]
_lib.parasail_matrix_free.restype = None

_lib.parasail_matrix_set_value.argtypes = [c_matrix_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.parasail_matrix_set_value.restype = None

_lib.parasail_matrix_copy.argtypes = [c_matrix_p]
_lib.parasail_matrix_copy.restype = c_matrix_p

_lib.parasail_nw_banded.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_matrix_p]
_lib.parasail_nw_banded.restype = c_result_p

def nw_banded(s1, s2, open, extend, k, matrix):
    return Result(_lib.parasail_nw_banded(b(s1), len(s1), b(s2), len(s2), open, extend, k, matrix), len(s1), len(s2))

_lib.parasail_result_get_traceback.argtypes = [c_result_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, c_matrix_p, ctypes.c_char, ctypes.c_char, ctypes.c_char]
_lib.parasail_result_get_traceback.restype = c_traceback_p

_lib.parasail_result_get_traceback_extra.argtypes = [c_result_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, c_matrix_p, ctypes.c_char, ctypes.c_char, ctypes.c_char, ctypes.c_int, ctypes.c_char_p]
_lib.parasail_result_get_traceback_extra.restype = c_traceback_p

_lib.parasail_traceback_free.argtypes = [c_traceback_p]
_lib.parasail_traceback_free.restype = None

_lib.parasail_cigar_encode.argtypes = [ctypes.c_uint32, ctypes.c_char]
_lib.parasail_cigar_encode.restype = ctypes.c_uint32

_lib.parasail_cigar_encode_string.argtypes = [ctypes.c_char_p]
_lib.parasail_cigar_encode_string.restype = c_cigar_p

_lib.parasail_cigar_decode_op.argtypes = [ctypes.c_uint32]
_lib.parasail_cigar_decode_op.restype = ctypes.c_char

_lib.parasail_cigar_decode_len.argtypes = [ctypes.c_uint32]
_lib.parasail_cigar_decode_len.restype = ctypes.c_uint32

_lib.parasail_cigar_decode.argtypes = [c_cigar_p]
_lib.parasail_cigar_decode.restype = ctypes.c_void_p

_lib.parasail_result_get_cigar.argtypes = [c_result_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, c_matrix_p]
_lib.parasail_result_get_cigar.restype = c_cigar_p

_lib.parasail_result_get_cigar_extra.argtypes = [c_result_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, c_matrix_p, ctypes.c_int, ctypes.c_char_p]
_lib.parasail_result_get_cigar_extra.restype = c_cigar_p

_lib.parasail_cigar_free.argtypes = [c_cigar_p]
_lib.parasail_cigar_free.restype = None

_lib.parasail_result_is_nw.argtypes = [c_result_p]
_lib.parasail_result_is_nw.restype = ctypes.c_int

_lib.parasail_result_is_sg.argtypes = [c_result_p]
_lib.parasail_result_is_sg.restype = ctypes.c_int

_lib.parasail_result_is_sw.argtypes = [c_result_p]
_lib.parasail_result_is_sw.restype = ctypes.c_int

_lib.parasail_result_is_saturated.argtypes = [c_result_p]
_lib.parasail_result_is_saturated.restype = ctypes.c_int

_lib.parasail_result_is_banded.argtypes = [c_result_p]
_lib.parasail_result_is_banded.restype = ctypes.c_int

_lib.parasail_result_is_scan.argtypes = [c_result_p]
_lib.parasail_result_is_scan.restype = ctypes.c_int

_lib.parasail_result_is_striped.argtypes = [c_result_p]
_lib.parasail_result_is_striped.restype = ctypes.c_int

_lib.parasail_result_is_diag.argtypes = [c_result_p]
_lib.parasail_result_is_diag.restype = ctypes.c_int

_lib.parasail_result_is_blocked.argtypes = [c_result_p]
_lib.parasail_result_is_blocked.restype = ctypes.c_int

_lib.parasail_result_is_stats.argtypes = [c_result_p]
_lib.parasail_result_is_stats.restype = ctypes.c_int

_lib.parasail_result_is_stats_table.argtypes = [c_result_p]
_lib.parasail_result_is_stats_table.restype = ctypes.c_int

_lib.parasail_result_is_stats_rowcol.argtypes = [c_result_p]
_lib.parasail_result_is_stats_rowcol.restype = ctypes.c_int

_lib.parasail_result_is_table.argtypes = [c_result_p]
_lib.parasail_result_is_table.restype = ctypes.c_int

_lib.parasail_result_is_rowcol.argtypes = [c_result_p]
_lib.parasail_result_is_rowcol.restype = ctypes.c_int

_lib.parasail_result_is_trace.argtypes = [c_result_p]
_lib.parasail_result_is_trace.restype = ctypes.c_int

_lib.parasail_result_get_score.argtypes = [c_result_p]
_lib.parasail_result_get_score.restype = ctypes.c_int

_lib.parasail_result_get_end_query.argtypes = [c_result_p]
_lib.parasail_result_get_end_query.restype = ctypes.c_int

_lib.parasail_result_get_end_ref.argtypes = [c_result_p]
_lib.parasail_result_get_end_ref.restype = ctypes.c_int

_lib.parasail_result_get_matches.argtypes = [c_result_p]
_lib.parasail_result_get_matches.restype = ctypes.c_int

_lib.parasail_result_get_similar.argtypes = [c_result_p]
_lib.parasail_result_get_similar.restype = ctypes.c_int

_lib.parasail_result_get_length.argtypes = [c_result_p]
_lib.parasail_result_get_length.restype = ctypes.c_int

_lib.parasail_result_get_score_table.argtypes = [c_result_p]
_lib.parasail_result_get_score_table.restype = c_int_p

_lib.parasail_result_get_matches_table.argtypes = [c_result_p]
_lib.parasail_result_get_matches_table.restype = c_int_p

_lib.parasail_result_get_similar_table.argtypes = [c_result_p]
_lib.parasail_result_get_similar_table.restype = c_int_p

_lib.parasail_result_get_length_table.argtypes = [c_result_p]
_lib.parasail_result_get_length_table.restype = c_int_p

_lib.parasail_result_get_score_row.argtypes = [c_result_p]
_lib.parasail_result_get_score_row.restype = c_int_p

_lib.parasail_result_get_matches_row.argtypes = [c_result_p]
_lib.parasail_result_get_matches_row.restype = c_int_p

_lib.parasail_result_get_similar_row.argtypes = [c_result_p]
_lib.parasail_result_get_similar_row.restype = c_int_p

_lib.parasail_result_get_length_row.argtypes = [c_result_p]
_lib.parasail_result_get_length_row.restype = c_int_p

_lib.parasail_result_get_score_col.argtypes = [c_result_p]
_lib.parasail_result_get_score_col.restype = c_int_p

_lib.parasail_result_get_matches_col.argtypes = [c_result_p]
_lib.parasail_result_get_matches_col.restype = c_int_p

_lib.parasail_result_get_similar_col.argtypes = [c_result_p]
_lib.parasail_result_get_similar_col.restype = c_int_p

_lib.parasail_result_get_length_col.argtypes = [c_result_p]
_lib.parasail_result_get_length_col.restype = c_int_p

_lib.parasail_result_get_trace_table.argtypes = [c_result_p]
_lib.parasail_result_get_trace_table.restype = c_int_p

_lib.parasail_result_get_trace_ins_table.argtypes = [c_result_p]
_lib.parasail_result_get_trace_ins_table.restype = c_int_p

_lib.parasail_result_get_trace_del_table.argtypes = [c_result_p]
_lib.parasail_result_get_trace_del_table.restype = c_int_p

class SSWResult:
    def __init__(self, pointer):
        self.pointer = pointer
        self._as_parameter_ = pointer
    def __del__(self):
        if _lib:
            _lib.parasail_result_ssw_free(self.pointer)
    @property
    def score1(self):
        return self.pointer[0].score1
    @property
    def ref_begin1(self):
        return self.pointer[0].ref_begin1
    @property
    def ref_end1(self):
        return self.pointer[0].ref_end1
    @property
    def read_begin1(self):
        return self.pointer[0].read_begin1
    @property
    def read_end1(self):
        return self.pointer[0].read_end1
    @property
    def cigar(self):
        return _make_nd_array(
            self.pointer[0].cigar,
            (self.cigarLen,),
            numpy.uint32)
    @property
    def cigarLen(self):
        return self.pointer[0].cigarLen

_lib.parasail_ssw.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_matrix_p]
_lib.parasail_ssw.restype = c_result_ssw_p

_lib.parasail_ssw_profile.argtypes = [c_profile_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.parasail_ssw_profile.restype = c_result_ssw_p

_lib.parasail_ssw_init.argtypes = [ctypes.c_char_p, ctypes.c_int, c_matrix_p, ctypes.c_int8]
_lib.parasail_ssw_init.restype = c_profile_p

_lib.parasail_result_ssw_free.argtype = [c_result_ssw_p]
_lib.parasail_result_ssw_free.restype = None

def ssw(s1, s2, open, extend, matrix):
    pointer = _lib.parasail_ssw(b(s1), len(s1), b(s2), len(s2), open, extend, matrix)
    if pointer:
        return SSWResult(pointer)
    else:
        return None

def ssw_profile(profile, s2, open, extend):
    pointer = _lib.parasail_ssw_profile(profile, b(s2), len(s2), open, extend)
    if pointer:
        return SSWResult(pointer)
    else:
        return None

def ssw_init(s1, matrix, score_size):
    s1b = b(s1)
    return Profile(_lib.parasail_ssw_init(s1b, len(s1), matrix, score_size), matrix, s1b)

_lib.parasail_sequences_from_file.argtype = [ctypes.c_char_p]
_lib.parasail_sequences_from_file.restype = c_sequences_p

class Sequence:
    def __init__(self, pointer):
        self.pointer = pointer
    def __len__(self):
        return int(self.pointer[0].seq.l)
    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                key = key + self.pointer[0].seq.l
            if key < 0 or key > self.pointer[0].seq.l:
                raise IndexError('Index out of range')
            return self.pointer[0].seq.s[key]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))
    def __str__(self):
        return self.pointer[0].seq.s
    @property
    def name(self):
        return self.pointer[0].name.s
    @property
    def comment(self):
        if self.pointer[0].comment.s:
            return self.pointer[0].comment.s
        else:
            return ""
    @property
    def seq(self):
        if self.pointer[0].seq.s:
            return self.pointer[0].seq.s
        else:
            return ""
    @property
    def qual(self):
        if self.pointer[0].qual.s:
            return self.pointer[0].qual.s
        else:
            return ""

class Sequences:
    def __init__(self, pointer):
        self.pointer = pointer
    def __del__(self):
        if _lib:
            _lib.parasail_sequences_free(self.pointer)
    def __len__(self):
        return int(self.pointer[0].l)
    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                key = key + self.pointer[0].l
            if key < 0 or key > self.pointer[0].l:
                raise IndexError('Index out of range')
            return Sequence(ctypes.pointer(self.pointer[0].seqs[key]))
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))
    @property
    def characters(self):
        return int(self.pointer[0].characters)
    @property
    def shortest(self):
        return int(self.pointer[0].shortest)
    @property
    def longest(self):
        return int(self.pointer[0].longest)
    @property
    def mean(self):
        return float(self.pointer[0].mean)
    @property
    def stddev(self):
        return float(self.pointer[0].stddev)

def sequences_from_file(filename):
    return Sequences(_lib.parasail_sequences_from_file(b(filename)))

# begin generated names here

_argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_matrix_p]
""")

# serial reference implementations
alg = ["nw", "sg", "sw", "sg_qb", "sg_qe", "sg_qx", "sg_db", "sg_de", "sg_dx", "sg_qb_de", "sg_qe_db"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol", "_trace"]
for a in alg:
    for s in stats:
        for t in table:
            if 'trace' in t and 'stats' in s: continue
            myprint("")
            myprint("_lib.parasail_"+a+s+t+".argtypes = _argtypes")
            myprint("_lib.parasail_"+a+s+t+".restype = c_result_p")
            myprint("def "+a+s+t+"(s1, s2, open, extend, matrix):")
            myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+"(")
            myprint(" "*8+"b(s1), len(s1), b(s2), len(s2), open, extend, matrix),")
            if 'trace' in t:
                myprint(" "*8+"len(s1), len(s2), s1, s2, matrix)")
            else:
                myprint(" "*8+"len(s1), len(s2))")

## serial scan reference implementations
alg = ["nw", "sg", "sw", "sg_qb", "sg_qe", "sg_qx", "sg_db", "sg_de", "sg_dx", "sg_qb_de", "sg_qe_db"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol", "_trace"]
for a in alg:
    for s in stats:
        for t in table:
            if 'trace' in t and 'stats' in s: continue
            myprint("")
            myprint("_lib.parasail_"+a+s+t+"_scan.argtypes = _argtypes")
            myprint("_lib.parasail_"+a+s+t+"_scan.restype = c_result_p")
            myprint("def "+a+s+t+"_scan(s1, s2, open, extend, matrix):")
            myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+"_scan(")
            myprint(" "*8+"b(s1), len(s1), b(s2), len(s2), open, extend, matrix),")
            if 'trace' in t:
                myprint(" "*8+"len(s1), len(s2), s1, s2, matrix)")
            else:
                myprint(" "*8+"len(s1), len(s2))")

# vectorized implementations
alg = ["nw", "sg", "sw", "sg_qb", "sg_qe", "sg_qx", "sg_db", "sg_de", "sg_dx", "sg_qb_de", "sg_qe_db"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol", "_trace"]
par = ["_scan", "_striped", "_diag"]
width = ["_64","_32","_16","_8","_sat"]
for a in alg:
    for s in stats:
        for t in table:
            if 'trace' in t and 'stats' in s: continue
            for p in par:
                for w in width:
                    myprint("")
                    myprint("_lib.parasail_"+a+s+t+p+w+".argtypes = _argtypes")
                    myprint("_lib.parasail_"+a+s+t+p+w+".restype = c_result_p")
                    myprint("def "+a+s+t+p+w+"(s1, s2, open, extend, matrix):")
                    myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+p+w+"(")
                    myprint(" "*8+"b(s1), len(s1), b(s2), len(s2), open, extend, matrix),")
                    if 'trace' in t:
                        myprint(" "*8+"len(s1), len(s2), s1, s2, matrix)")
                    else:
                        myprint(" "*8+"len(s1), len(s2))")

myprint("""
_argtypes = [c_profile_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
""")

# vectorized profile implementations
alg = ["nw", "sg", "sw", "sg_qb", "sg_qe", "sg_qx", "sg_db", "sg_de", "sg_dx", "sg_qb_de", "sg_qe_db"]
stats = ["", "_stats"]
table = ["", "_table", "_rowcol", "_trace"]
par = ["_scan_profile", "_striped_profile"]
width = ["_64","_32","_16","_8","_sat"]
for a in alg:
    for s in stats:
        for t in table:
            if 'trace' in t and 'stats' in s: continue
            for p in par:
                for w in width:
                    myprint("")
                    myprint("_lib.parasail_"+a+s+t+p+w+".argtypes = _argtypes")
                    myprint("_lib.parasail_"+a+s+t+p+w+".restype = c_result_p")
                    myprint("def "+a+s+t+p+w+"(profile, s2, open, extend):")
                    myprint(" "*4+"return Result(_lib.parasail_"+a+s+t+p+w+"(")
                    myprint(" "*8+"profile, b(s2), len(s2), open, extend),")
                    if 'trace' in t:
                        myprint(" "*8+"len(profile.s1), len(s2), profile.s1, s2, profile.matrix)")
                    else:
                        myprint(" "*8+"len(profile.s1), len(s2))")

