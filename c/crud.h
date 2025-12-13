#ifndef CRUD_H
#define CRUD_H

#include "database.h"
#include "models.h"
#include <sqlite3.h>

// Helper function to get next ID
char* get_next_id(sqlite3* db, const char* table_name, const char* prefix);

// User CRUD operations
int create_user(sqlite3* db, const char* firstname, const char* lastname, 
                const char* date_of_birth, const char* address, double balance, User* user);
int get_user(sqlite3* db, const char* user_id, User* user);
int get_all_users(sqlite3* db, User** users, int* count);
int update_user(sqlite3* db, const char* user_id, const char* firstname, 
                const char* lastname, const char* date_of_birth, 
                const char* address, double balance);
int delete_user(sqlite3* db, const char* user_id);

// Company CRUD operations
int create_company(sqlite3* db, const char* name, const char* location, Company* company);
int get_company(sqlite3* db, const char* company_id, Company* company);
int get_all_companies(sqlite3* db, Company** companies, int* count);
int update_company(sqlite3* db, const char* company_id, const char* name, const char* location);
int delete_company(sqlite3* db, const char* company_id);

// Transaction CRUD operations
int create_transaction(sqlite3* db, const char* user_id, const char* company_id,
                       int number_of_shares, const char* transaction_datetime, Transaction* transaction);
int get_transaction(sqlite3* db, const char* transaction_id, Transaction* transaction);
int get_all_transactions(sqlite3* db, Transaction** transactions, int* count);
int get_transactions_by_user(sqlite3* db, const char* user_id, Transaction** transactions, int* count);
int get_transactions_by_company(sqlite3* db, const char* company_id, Transaction** transactions, int* count);
int update_transaction(sqlite3* db, const char* transaction_id, const char* user_id,
                      const char* company_id, int number_of_shares, const char* transaction_datetime);
int delete_transaction(sqlite3* db, const char* transaction_id);

#endif // CRUD_H


