CC = C:/msys64/ucrt64/bin/gcc.exe
CFLAGS  = -Wall -Wextra -std=c11 -g
LDFLAGS = -fno-lto -lsqlite3
TARGET = app
SOURCES = main.c database.c crud.c
OBJECTS = $(SOURCES:.c=.o)

# Default target
all: $(TARGET)

# Build the executable
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET) $(LDFLAGS)

# Compile source files to object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(OBJECTS) $(TARGET) app.db

# Install dependencies (for Linux/Mac)
install-deps:
	@echo "Installing SQLite3 development libraries..."
	@if command -v apt-get > /dev/null; then \
		sudo apt-get install -y libsqlite3-dev; \
	elif command -v brew > /dev/null; then \
		brew install sqlite3; \
	elif command -v yum > /dev/null; then \
		sudo yum install -y sqlite-devel; \
	else \
		echo "Please install SQLite3 development libraries manually"; \
	fi

# Run the application
run: $(TARGET)
	./$(TARGET)

.PHONY: all clean install-deps run


