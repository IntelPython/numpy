pushd mkl_random
if %PY_VER%==2.7 (
    set VS=vs2008
    set ICC_COMP_BAT="C:\Program Files (x86)\Intel\Composer XE 2013 SP1\bin\compilervars_arch.bat"
) else (
    set VS=vs2015
    set ICC_COMP_BAT="C:\Program Files (x86)\IntelSWTools\parallel_studio_xe_2016.3.059\compilers_and_libraries_2016\windows\bin\compilervars_arch.bat"
)

call %ICC_COMP_BAT% intel64 %VS%
if errorlevel 1 exit 1
set CC=icl
set LD=xilink

set CFLAGS=-I%PREFIX%\Library\include %CFLAGS%
set LDFLAGS=/LIBPATH:%PREFIX%\Library\lib %LDFLAGS%
rem set MKLROOT=%PREFIX%\Library
%PYTHON% setup.py config --compiler=intelemw install --old-and-unmanageable
if errorlevel 1 exit 1
%PYTHON% setup.py bdist_wheel
if errorlevel 1 exit 1
copy dist\mkl_random*.whl ..\..\
if errorlevel 1 exit 1
popd
