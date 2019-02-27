import os, platform
from os.path import join as jp

IS_WIN = platform.system() == 'Windows'
IS_LIN = platform.system() == 'Linux'
IS_MAC = platform.system() == 'Darwin'

def mkl_strings_for_site_cfg(mklroot):
    iccroot = os.path.dirname(mklroot)
    win_lin_lib_dir = jp(mklroot, 'lib', 'intel64')
    mac_lib_dir = jp(mklroot, 'lib')
    win_compiler_libs = jp(iccroot, 'compiler', 'lib', 'intel64')
    inc_dir = jp(mklroot, 'include')
    conf_inc_dir = inc_dir

    assert os.path.exists(iccroot), 'path: ' + str(iccroot)
    assert os.path.exists(inc_dir), 'path: ' + inc_dir

    if IS_WIN:
        assert os.path.exists(win_lin_lib_dir), 'path: ' + win_lin_lib_dir
        assert os.path.exists(win_compiler_libs), 'path: ' + win_compiler_libs
        conf_lib_dir = win_lin_lib_dir + ';' + win_compiler_libs
        conf_inc_dir = inc_dir + ';' + jp(iccroot, 'compiler', 'include')
    elif IS_MAC:
        assert os.path.exists(mac_lib_dir), 'path: ' + mac_lib_dir
        conf_lib_dir = mac_lib_dir
    elif IS_LIN:
        assert os.path.exists(win_lin_lib_dir), 'path: ' + win_lin_lib_dir
        conf_lib_dir = win_lin_lib_dir

    conf = '\n'.join(['[mkl]',
                      'library_dirs = ' + conf_lib_dir,
                      'include_dirs = ' + conf_inc_dir,
                      'mkl_libs = mkl_rt',
                      'lapack_libs = mkl_rt', ])
    return conf

def get_mkl_version_header(mklroot):
    import sys, re
    if sys.platform == 'win32':
        prefix = jp(mklroot, 'Library')
    else:
        prefix = mklroot

    header_path = jp(prefix, 'include', 'mkl.h')
    pat = re.compile(r'#define\s+__INTEL_MKL(\w*)__\s+(\d+)')
    parts = {}
    try:
        for line in open(header_path):
            m = pat.match(line.strip())
            if m:
                parts[m.group(1)] = m.group(2)
    except IOError:
        return '<NO MKL HEADER FOUND>'
    return '.'.join(parts[k] for k in ('', '_MINOR', '_UPDATE'))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('mklroot', help='MKL install dir')
    parser.add_argument('-c', '--config', help='file to store site.cfg in')
    args = parser.parse_args()

    with open(args.config, "w") as f:
        f.write(mkl_strings_for_site_cfg(args.mklroot))
    print(get_mkl_version_header(args.mklroot))
