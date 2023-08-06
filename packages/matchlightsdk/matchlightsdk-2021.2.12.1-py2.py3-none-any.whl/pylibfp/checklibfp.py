#!/bin/python3

__author__ = "Manoj Kumar Arram"


from ctypes import cdll, c_char, c_char_p, c_int, create_string_buffer, Structure, POINTER
import pkg_resources
from os import path
import json


def get_library_path(library_filename):
    return pkg_resources.resource_filename('pylibfp', path.join('lib', library_filename))


_libfp = cdll.LoadLibrary(get_library_path("libfpl64.so"))

class ResultStruct(Structure):
  _fields_ = [("err", c_int), ("data", c_char_p)]


_libfp.fingerprint.argtypes = [POINTER(c_char), c_int, c_int]
_libfp.fingerprint.restype = POINTER(ResultStruct)

_libfp.fingerprint_chunk.argtypes = [POINTER(c_char), c_int]
_libfp.fingerprint_chunk.restype = c_char_p

_libfp.fingerprint_email_terbiumtwox.argtypes = [POINTER(c_char)]
_libfp.fingerprint_email_terbiumtwox.restype = c_char_p

_libfp.fingerprint_email_fromsha1.argtypes = [POINTER(c_char)]
_libfp.fingerprint_email_fromsha1.restype = c_char_p

_libfp.fingerprint_email_sha1.argtypes = [POINTER(c_char)]
_libfp.fingerprint_email_sha1.restype = c_char_p

_libfp.clean_string.argtypes = [POINTER(c_char), c_int]
_libfp.clean_string.restype = c_char_p

_libfp.assets_from_name.argtypes = [POINTER(c_char), POINTER(c_char),
    POINTER(c_char), POINTER(c_char), POINTER(c_char)]
_libfp.assets_from_name.restype = c_char_p

_libfp.assets_from_address.argtypes = [POINTER(c_char), POINTER(c_char),
    POINTER(c_char)]
_libfp.assets_from_address.restype = c_char_p

_libfp.assets_from_city_state_zip.argtypes = [POINTER(c_char), POINTER(c_char),
    POINTER(c_char), POINTER(c_char), POINTER(c_char)]
_libfp.assets_from_city_state_zip.restype = c_char_p

_libfp.assets_from_email_address.argtypes = [POINTER(c_char), POINTER(c_char),
    POINTER(c_char)]
_libfp.assets_from_email_address.restype = c_char_p

_libfp.assets_from_ssn.argtypes = [POINTER(c_char), POINTER(c_char),
    POINTER(c_char)]
_libfp.assets_from_ssn.restype = c_char_p

_libfp.assets_from_phone_number.argtypes = [POINTER(c_char), POINTER(c_char),
    POINTER(c_char)]
_libfp.assets_from_phone_number.restype = c_char_p

_libfp.assets_from_credit_card.argtypes = [POINTER(c_char), POINTER(c_char), POINTER(c_char)]
_libfp.assets_from_credit_card.restype = c_char_p

_libfp.assets_from_medicare_id.argtypes = [POINTER(c_char), POINTER(c_char), POINTER(c_char)]
_libfp.assets_from_medicare_id.restype = c_char_p

_libfp.assets_from_passport.argtypes = [POINTER(c_char), POINTER(c_char), POINTER(c_char)]
_libfp.assets_from_passport.restype = c_char_p

_libfp.assets_from_iban.argtypes = [POINTER(c_char), POINTER(c_char), POINTER(c_char)]
_libfp.assets_from_iban.restype = c_char_p

MODE_TEXT = 0
MODE_CODE = 1
MODE_DIGITS = 2

ML_HASH_LENGTH = 32

OPTIONS_BOOLEAN = 1
OPTIONS_RAW = 2
OPTIONS_TILED = 4
OPTIONS_STORABLENGRAMS = 8
OPTIONS_PARSEONLY = 16

ERROR_PADDING = 1
ERROR_PADDING_MSG = "Unable to fingerprint chunk: {}"


def _ensure_unicode(v):
    if hasattr(v, "decode"):
        return v.decode("utf-8")
    else:
        return v


def fingerprints_pii_name_variants(first_name, middle_name, last_name):
    assets_json = _ensure_unicode(_libfp.assets_from_name(
            b"temporary", b"0", first_name, middle_name, last_name))
    assets = json.loads(assets_json)
    return [[_ensure_unicode(fp) for fp in asset["fingerprints"]]
            for asset in assets]


print(fingerprints_pii_name_variants("Manoj", "Kumar", "Arram"))
