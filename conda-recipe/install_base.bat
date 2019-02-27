
call activate_compiler.bat
if errorlevel 1 exit 1

set CC=icl
set LD=xilink

%PYTHON% %RECIPE_DIR%\cio_files\mkl_version.py numpy\__init__.py
if errorlevel 1 exit 1

copy %RECIPE_DIR%\cio_files\numpy\site-mkl-%SUBDIR%.cfg site.cfg
if errorlevel 1 exit 1

sed -i 's,libs =.*,libs = mkl_rt,g' site.cfg
@rem sed -i 's#libs =.*#libs = mkl_intel_lp64_dll, mkl_intel_thread_dll, mkl_core_dll, libiomp5md#g' site.cfg
if errorlevel 1 exit 1


%PYTHON% %RECIPE_DIR%\cio_files\replace.py @PREFIX@ "%PREFIX%" site.cfg
if errorlevel 1 exit 1

set CFLAGS=-DNDEBUG -I%PREFIX%\Library\include %CFLAGS%
%PYTHON% setup.py config_cc --compiler=intelemw build --force install --old-and-unmanageable
if errorlevel 1 exit 1
%PYTHON% setup.py bdist_wheel
if errorlevel 1 exit 1
copy dist\numpy-1*.whl ..\..\
if errorlevel 1 exit 1
