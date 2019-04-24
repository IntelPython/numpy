#!/bin/bash

if [ $NOMKL == 1 ]
then # Non-MKL
    if [ `uname` == Linux ]; then
        SITE_CFG="site-openblas-linux.cfg"
    else
        SITE_CFG="site-empty.cfg"
    fi
else # MKL
    $PYTHON $RECIPE_DIR/cio_files/mkl_version.py ./numpy/__init__.py
    if [ `uname` == Darwin ]; then
        export ATLAS=1
        export LDFLAGS="-headerpad_max_install_names $LDFLAGS"
    fi
    SITE_CFG="site-mkl-$SUBDIR.cfg"
fi

sed -e "s,@PREFIX@,$PREFIX," <$RECIPE_DIR/cio_files/numpy/$SITE_CFG >site.cfg

if [ `uname` == Darwin ]; then
    source /localdisk/tools/intel/compilers_and_libraries_16.0.3/mac/bin/compilervars.sh intel64
    sed -i -e 's/mkl_libs =.*/mkl_libs = mkl_rt/g' site.cfg
    sed -i -e 's/lapack_libs =.*/lapack_libs = mkl_rt/g' site.cfg
    export MACOSX_DEPLOYMENT_TARGET=10.10
else
    # source /localdisk/tools/intel/compilers_and_libraries_16.0.3/linux/bin/compilervars.sh intel64
    sed -i 's,libs =.*,libs = mkl_rt,g' site.cfg
fi

if [ ! -f site.cfg ]; then
    echo "ERROR: *** site.cfg missing ***"
    exit 1
fi

CFLAGS="-DNDEBUG -I$PREFIX/include $CFLAGS" $PYTHON setup.py config_cc --compiler=intelem config_fc --fcompiler=intelem build --force install --old-and-unmanageable
$PYTHON setup.py bdist_wheel
cp dist/numpy*.whl ../../
