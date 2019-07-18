#!/bin/bash -x

pushd mkl_random
if [ `uname` == Darwin ]; then
    source /localdisk/tools/intel/compilers_and_libraries_16.0.3/mac/bin/compilervars.sh intel64
    export MACOSX_DEPLOYMENT_TARGET=10.10
    export LDFLAGS="-headerpad_max_install_names $LDFLAGS"
fi

export CFLAGS="-I$PREFIX/include $CFLAGS"
export LDFLAGS="-L$PREFIX/lib $LDFLAGS"
export CC=icc
export LDSHARED="icc -shared"

$PYTHON setup.py config --compiler=intelem --fcompiler=intelem build install --old-and-unmanageable
if [ `uname` == Linux ]; then
    intel-libpatch.sh
fi
$PYTHON setup.py bdist_wheel
cp dist/mkl_random*.whl ../../../
popd

