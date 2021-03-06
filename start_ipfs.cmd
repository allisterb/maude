@echo off
@setlocal
set ERROR_CODE=0

if not "%1"=="" (
   set LOG_FILE=%1
) else (
    set LOG_FILE=ipfs.log
)
if not "%2"=="" (
   set IPFS_CMD=%2
) else (
    set IPFS_CMD=ipfs
)

call set_ipfs_logging %LOG_FILE%
if not %ERRORLEVEL% == 0 goto SetLogFileError

start %IPFS_CMD% daemon --enable-pubsub-experiment --upgrade-cidv0-in-output
if not %ERRORLEVEL% == 0 goto StartError

echo Started IPFS daemon configured for maud3 monitoring. 
goto End

:SetLogFileError
echo Could not set IPFS daemon log file to %LOG_FILE%.
set ERROR_CODE=1
goto End

:StartError
echo Could not start the IPFS daemon using %IPFS_CMD% daemon --enable-pubsub-experiment --upgrade-cidv0-in-output.
set ERROR_CODE=2
goto End

:End
@endlocal
exit /b %ERROR_CODE%

