# Python Implementation
Author: Srimathi Siva

This is the Python implementation of the User & Company Management System.

## Features

- Full CRUD operations for Users, Companies, and Transactions
- SQLite database with SQLAlchemy ORM
- Graphical User Interface (GUI) with tkinter
- Comprehensive test suite
- Auto-generated IDs: U1, U2... for users, C1, C2... for companies, T1, T2... for transactions

## Requirements

- Python 3.7+
- SQLAlchemy
- tkinter (usually included with Python)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the GUI Application

**Windows:**
```bash
python gui.py
```
or double-click `start.bat`

**Linux/Mac:**
```bash
python gui.py
```
or run `./start.sh`

### Running the Command-Line Example

```bash
python main.py
```

### Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
python/
├── main.py          # Example usage and demonstration
├── gui.py           # Graphical user interface
├── database.py      # Database configuration
├── models.py        # SQLAlchemy models
├── crud.py          # CRUD operations
├── requirements.txt # Python dependencies
├── start.bat        # Windows launcher
├── start.sh         # Linux/Mac launcher
└── tests/           # Test suite
```

## Database

The application uses SQLite3 and creates a database file `app.db` in the project root.


