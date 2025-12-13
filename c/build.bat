@echo off
echo Checking for C compiler...

REM Check for GCC (MinGW)
where gcc >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found GCC compiler
    echo Building C application...
    gcc -Wall -Wextra -std=c11 main.c database.c crud.c -o app.exe -lsqlite3
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Build successful! Run app.exe to start the application.
    ) else (
        echo.
        echo Build failed! Make sure SQLite3 libraries are available.
        echo You may need to download sqlite3.dll and place it in the same folder.
    )
    goto :end
)

REM Check for Clang
where clang >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Clang compiler
    echo Building C application...
    clang -Wall -Wextra -std=c11 main.c database.c crud.c -o app.exe -lsqlite3
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Build successful! Run app.exe to start the application.
    ) else (
        echo.
        echo Build failed! Make sure SQLite3 libraries are available.
    )
    goto :end
)

REM Check for MSVC (cl.exe)
where cl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found MSVC compiler
    echo Building C application...
    cl main.c database.c crud.c /Fe:app.exe /link sqlite3.lib
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Build successful! Run app.exe to start the application.
    ) else (
        echo.
        echo Build failed! Make sure SQLite3 libraries are available.
    )
    goto :end
)

echo.
echo ========================================
echo No C compiler found!
echo ========================================
echo.
echo Please install one of the following:
echo.
echo OPTION 1: MinGW-w64 (Recommended)
echo   1. Download from: https://www.mingw-w64.org/downloads/
echo   2. Or use MSYS2: https://www.msys2.org/
echo   3. Or use Chocolatey: choco install mingw
echo.
echo OPTION 2: Visual Studio Build Tools
echo   1. Download from: https://visualstudio.microsoft.com/downloads/
echo   2. Install "Desktop development with C++" workload
echo.
echo OPTION 3: Use WSL (Windows Subsystem for Linux)
echo   1. Install WSL: wsl --install
echo   2. Then use: cd c && make
echo.
echo After installing, restart this script.
echo.
pause
:end
