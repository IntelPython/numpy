import ctypes
import platform
import argparse
import os.path
import re

def _find_mkl():
    _pl = platform.system()
    if _pl == 'Linux':
        mkl = ctypes.cdll.LoadLibrary('libmkl_rt.so')
    elif _pl == 'Windows':
        mkl = ctypes.cdll.LoadLibrary('mkl_rt.dll')
    elif _pl == 'Darwin':
        mkl = ctypes.cdll.LoadLibrary('libmkl_rt.dylib')

    return mkl

class _MKL_Version(ctypes.Structure):
    _fields_ = [('MajorVersion', ctypes.c_int),
                ('MinorVersion', ctypes.c_int),
                ('UpdateVersion', ctypes.c_int),
                ('Build', ctypes.c_char_p),
                ('Platform', ctypes.c_char_p),
                ('Processor', ctypes.c_char_p)]


def mkl_version_struct_values(mkl):
    """
    Get values of MKL self-reported version struct.

    Returns tuple of major version, minor version, update version,
            build status, platform and processor.

    [1] https://software.intel.com/en-us/mkl-developer-reference-c-mkl-get-version"""
    _vf = mkl.mkl_get_version
    _vf.restypes = None
    _mkl_version_p = ctypes.POINTER(_MKL_Version)
    _vf.argtypes = (_mkl_version_p,)
    _mkl_version = _MKL_Version()
    _vf(ctypes.byref(_mkl_version))
    return (_mkl_version.MajorVersion, 
            _mkl_version.MinorVersion, 
            _mkl_version.UpdateVersion,
            _mkl_version.Build,
            _mkl_version.Platform,
            _mkl_version.Processor)

def make_mkl_version(mkl):
    mkl_ver = mkl_version_struct_values(mkl)
    return '.'.join([ str(i) for i in mkl_ver[:3] ])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Replace '__MKL_VERSION__' string in input file with actual value")
    parser.add_argument('fileName', type=str, help="file to process")
    
    args = parser.parse_args()
    if not os.path.exists(args.fileName):
        raise ValueError("File {} is expected to exist.".format(args.fileName))

    mkl_ver_str = make_mkl_version(_find_mkl())
    with open(args.fileName, 'r') as fh:
        fileContent = fh.read()
    
    fileContentNew = fileContent.replace('__MKL_VERSION__', mkl_ver_str)

    if(fileContentNew != fileContent):
        with open(args.fileName, 'w') as fh:
            fh.write(fileContentNew)

