#include "database.h"

sqlite3* db_connect(const char* db_path) {
    sqlite3* db;
    int rc = sqlite3_open(db_path, &db);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return NULL;
    }
    
    return db;
}

void db_close(sqlite3* db) {
    if (db) {
        sqlite3_close(db);
    }
}

int db_init(sqlite3* db) {
    char* err_msg = 0;
    
    // Create users table
    const char* create_users = 
        "CREATE TABLE IF NOT EXISTS users ("
        "user_id TEXT PRIMARY KEY,"
        "firstname TEXT NOT NULL,"
        "lastname TEXT NOT NULL,"
        "date_of_birth DATE NOT NULL,"
        "address TEXT NOT NULL,"
        "balance NUMERIC(10,2) DEFAULT 0.00"
        ");";
    
    int rc = sqlite3_exec(db, create_users, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error (users): %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    // Create companies table
    const char* create_companies = 
        "CREATE TABLE IF NOT EXISTS companies ("
        "company_id TEXT PRIMARY KEY,"
        "name TEXT NOT NULL,"
        "location TEXT NOT NULL"
        ");";
    
    rc = sqlite3_exec(db, create_companies, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error (companies): %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    // Create transactions table
    const char* create_transactions = 
        "CREATE TABLE IF NOT EXISTS transactions ("
        "transaction_id TEXT PRIMARY KEY,"
        "user_id TEXT NOT NULL,"
        "company_id TEXT NOT NULL,"
        "number_of_shares INTEGER NOT NULL,"
        "transaction_datetime DATETIME NOT NULL,"
        "FOREIGN KEY(user_id) REFERENCES users(user_id),"
        "FOREIGN KEY(company_id) REFERENCES companies(company_id)"
        ");";
    
    rc = sqlite3_exec(db, create_transactions, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error (transactions): %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}


