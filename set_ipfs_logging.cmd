@echo off
if not "%1"=="" (
   set GOLOG_FILE=%1
) else (
    set GOLOG_FILE=ipfs.log
)
set GOLOG_LOG_FMT=json
set GOLOG_OUTPUT=stdout+file
set GOLOG_LOG_LEVEL=error,provider.simple=info,provider.queue=info,reprovider.simple=info

echo IPFS will log to file %GOLOG_FILE% in JSON format using log level INFO for selected subsystems.