@echo off
setlocal enabledelayedexpansion

:: Check if the required arguments are passed
if "%~1"=="" (
    echo Usage: %0 -fp ^<filepath^> -e ^<extension^>
    exit /b 1
)

:: Initialize variables
set filepath=
set extension=

:: Parse arguments
:parse
if "%~1"=="" goto check_args
if "%~1"=="-fp" (
    set filepath=%~2
    shift
    shift
    goto parse
)
if "%~1"=="-e" (
    set extension=%~2
    shift
    shift
    goto parse
)
echo Unknown parameter passed: %~1
exit /b 1

:check_args
:: Validate filepath
if not exist "!filepath!" (
    echo File not found: !filepath!
    exit /b 1
)

echo Current directory: %cd%

:: Execute the Docker command with the validated arguments
docker run -it ^
  -v "%cd%\output:/app/output/" ^
  -v "%cd%\!filepath!:/app/!filepath!" ^
  proto_compiler python3 cli.py -fp "!filepath!" -e "!extension!"

endlocal
