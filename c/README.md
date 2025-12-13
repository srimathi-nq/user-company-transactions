# C Implementation

This is the C implementation of the User & Company Management System.

## Features

- Full CRUD operations for Users, Companies, and Transactions
- SQLite database backend
- Console-based interface
- Auto-generated IDs: U1, U2... for users, C1, C2... for companies, T1, T2... for transactions

## Requirements

- GCC compiler (or Clang/MSVC)
- SQLite3 development libraries

### Installing on Windows

**See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed Windows installation instructions.**

Quick options:
1. **MSYS2** (Recommended): https://www.msys2.org/
2. **Chocolatey**: `choco install mingw sqlite`
3. **WSL**: `wsl --install` then use Linux instructions

### Installing Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install build-essential libsqlite3-dev
```

**Linux (Fedora/RHEL):**
```bash
sudo yum install gcc sqlite-devel
```

**macOS:**
```bash
brew install sqlite3
```

## Building

### Using Makefile (Linux/Mac):

```bash
make
```

Or use the install-deps target to install dependencies:
```bash
make install-deps
make
```

### Using Build Script (Windows):

```bash
build.bat
```

The script will automatically detect GCC, Clang, or MSVC.

### Manual Compilation:

**Linux/Mac:**
```bash
gcc -Wall -Wextra -std=c11 main.c database.c crud.c -o app -lsqlite3
```

**Windows (MinGW):**
```bash
gcc -Wall -Wextra -std=c11 main.c database.c crud.c -o app.exe -lsqlite3
```

**Windows (MSVC):**
```bash
cl main.c database.c crud.c /Fe:app.exe /link sqlite3.lib
```

## Running

**Linux/Mac:**
```bash
./app
```

**Windows:**
```bash
app.exe
```

## Project Structure

```
c/
├── main.c          # Main application entry point
├── database.h      # Database connection and initialization
├── database.c      # Database implementation
├── models.h        # Data structures (User, Company, Transaction)
├── crud.h          # CRUD operation declarations
├── crud.c          # CRUD operation implementations
├── Makefile        # Build configuration (Linux/Mac)
├── build.bat       # Build script (Windows)
├── README.md       # This file
└── INSTALL_WINDOWS.md  # Windows installation guide
```

## Database

The application uses SQLite3 and creates a database file `app.db` in the current directory.

## Notes

- The C implementation provides the same functionality as the Python version
- All CRUD operations are fully implemented
- Foreign key relationships are maintained
- Cascade deletion is implemented (deleting a user/company also deletes related transactions)
- The executable is standalone and can be distributed independently
