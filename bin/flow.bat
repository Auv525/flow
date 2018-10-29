set BIN_PATH=%~dp0
set PYLIB_PATH=%BIN_PATH%..\pylib
set PYTHONPATH=%PYLIB_PATH%;%PYTHONPATH%

set FLOW_PATH=%BIN_PATH%flow.py
C:\python27\python.exe %FLOW_PATH% %*
