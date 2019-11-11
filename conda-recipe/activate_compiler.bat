rem Example of activating Intel(R) Compiler on Windows
rem Adjust the path as necessary


if %PY_VER%==2.7 (
    set VS=vs2008
    set ICC_COMP_BAT="C:\Program Files (x86)\Intel\Composer XE 2013 SP1\bin\compilervars_arch.bat"
) else (
    set VS=vs2015
    set ICC_COMP_BAT="C:\Program Files (x86)\IntelSWTools\parallel_studio_xe_2016.3.059\compilers_and_libraries_2016\windows\bin\compilervars_arch.bat"
)

call %ICC_COMP_BAT% intel64 %VS%
if errorlevel 1 exit 1
