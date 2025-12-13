#ifndef DATABASE_H
#define DATABASE_H

#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Database connection
sqlite3* db_connect(const char* db_path);
void db_close(sqlite3* db);
int db_init(sqlite3* db);

#endif // DATABASE_H


