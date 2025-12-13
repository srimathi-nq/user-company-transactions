# Installing C Compiler on Windows

This guide will help you install a C compiler on Windows to build the application.

## Option 1: MinGW-w64 (Recommended - Easiest)

### Method A: Using MSYS2 (Recommended)

1. **Download MSYS2:**
   - Go to https://www.msys2.org/
   - Download and run the installer
   - Follow the installation wizard

2. **Install GCC:**
   - Open MSYS2 terminal (or MSYS2 UCRT64)
   - Run: `pacman -S mingw-w64-ucrt-x86_64-gcc`
   - Run: `pacman -S mingw-w64-ucrt-x86_64-sqlite`

3. **Add to PATH:**
   - Add `C:\msys64\ucrt64\bin` to your Windows PATH
   - Or use MSYS2 terminal to build

4. **Build the application:**
   ```bash
   cd /c/Users/YourName/Documents/pythonproject/c
   gcc -Wall -Wextra -std=c11 main.c database.c crud.c -o app.exe -lsqlite3
   ```

### Method B: Using Chocolatey

1. **Install Chocolatey** (if not installed):
   - Open PowerShell as Administrator
   - Run: `Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`

2. **Install MinGW:**
   ```powershell
   choco install mingw
   ```

3. **Install SQLite:**
   ```powershell
   choco install sqlite
   ```

4. **Build:**
   ```bash
   cd c
   build.bat
   ```

### Method C: Direct Download

1. **Download MinGW-w64:**
   - Go to https://winlibs.com/
   - Download the latest release (e.g., "GCC 13.2.0 + LLVM/Clang/LLD/LLDB 17.0.6 + MinGW-w64 11.0.1")
   - Extract to `C:\mingw64`

2. **Add to PATH:**
   - Add `C:\mingw64\bin` to your Windows PATH environment variable
   - Restart your terminal

3. **Download SQLite:**
   - Download from https://www.sqlite.org/download.html
   - Extract `sqlite3.dll` to `C:\mingw64\bin` or your project folder

4. **Build:**
   ```bash
   cd c
   build.bat
   ```

## Option 2: Visual Studio Build Tools

1. **Download Visual Studio:**
   - Go to https://visualstudio.microsoft.com/downloads/
   - Download "Build Tools for Visual Studio"

2. **Install:**
   - Run the installer
   - Select "Desktop development with C++" workload
   - Install

3. **Build:**
   - Open "Developer Command Prompt for VS"
   - Navigate to project: `cd C:\Users\YourName\Documents\pythonproject\c`
   - Run: `cl main.c database.c crud.c /Fe:app.exe /link sqlite3.lib`
   - (You'll need to download SQLite3 library files separately)

## Option 3: WSL (Windows Subsystem for Linux)

1. **Install WSL:**
   ```powershell
   wsl --install
   ```
   Restart your computer when prompted.

2. **Open WSL terminal:**
   - Type `wsl` in PowerShell or Command Prompt

3. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install build-essential libsqlite3-dev
   ```

4. **Build:**
   ```bash
   cd /mnt/c/Users/YourName/Documents/pythonproject/c
   make
   ./app
   ```

## Quick Test

After installation, test if GCC is available:

```bash
gcc --version
```

If it shows version information, you're ready to build!

## Troubleshooting

### "sqlite3.h: No such file or directory"
- You need SQLite3 development headers
- For MinGW: Install `mingw-w64-x86_64-sqlite3` package
- Or download SQLite3 source and extract headers

### "undefined reference to sqlite3_*"
- You need SQLite3 library
- Download `sqlite3.dll` and `libsqlite3.a` (or `.lib`)
- Place in your compiler's library path

### "gcc: command not found"
- Make sure GCC is in your PATH
- Restart your terminal after adding to PATH
- Try using the full path: `C:\mingw64\bin\gcc.exe`

## Recommended Setup

For easiest setup, I recommend **MSYS2** (Option 1, Method A) as it provides:
- Easy package management
- Pre-built SQLite3 libraries
- All dependencies in one place
- Works seamlessly with Windows


