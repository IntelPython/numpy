import platform
import argparse
import os.path
import re
import mkl


def mkl_version_struct_values():
    return mkl.get_version()


def make_mkl_version():
    mkl_ver_dict = mkl_version_struct_values()
    mkl_ver = [
        mkl_ver_dict['MajorVersion'],
        mkl_ver_dict['MinorVersion'],
        mkl_ver_dict['UpdateVersion'] ]
    return '.'.join([ str(i) for i in mkl_ver ])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Replace '__MKL_VERSION__' string in input file with actual value")
    parser.add_argument('fileName', type=str, help="file to process")
    
    args = parser.parse_args()
    if not os.path.exists(args.fileName):
        raise ValueError("File {} is expected to exist.".format(args.fileName))

    mkl_ver_str = make_mkl_version()
    print(mkl_ver_str)
    with open(args.fileName, 'r') as fh:
        fileContent = fh.read()
    
    fileContentNew = fileContent.replace('__MKL_VERSION__', mkl_ver_str)

    if(fileContentNew != fileContent):
        with open(args.fileName, 'w') as fh:
            fh.write(fileContentNew)

