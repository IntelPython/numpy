#!/bin/bash -x

pushd mkl_fft
if [ `uname` == Darwin ]; then
    source /localdisk/tools/intel/compilers_and_libraries_16.0.3/mac/bin/compilervars.sh intel64
    export MACOSX_DEPLOYMENT_TARGET=10.10
    export LDFLAGS="-headerpad_max_install_names $LDFLAGS"
fi

LDFLAGS="-L$PREFIX/lib $LDFLAGS" CFLAGS="-I$PREFIX/include $CFLAGS" $PYTHON setup.py build --force --compiler=intelem install --old-and-unmanageable
if [ `uname` == Linux ]; then
    intel-libpatch.sh
fi
$PYTHON setup.py bdist_wheel
cp dist/mkl_fft*.whl ../../../
popd

