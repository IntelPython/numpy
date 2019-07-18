@rem See the remark in install_base.sh for explanation
copy %RECIPE_DIR%\intel_tester_config.py %SRC_DIR%
if errorlevel 1 exit 1
