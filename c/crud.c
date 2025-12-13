#include "crud.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

// Helper function to get next ID
char* get_next_id(sqlite3* db, const char* table_name, const char* prefix) {
    char sql[200];
    sqlite3_stmt* stmt;
    char* id = (char*)malloc(20);
    int max_num = 0;
    
    snprintf(sql, sizeof(sql), "SELECT %s_id FROM %s", 
             (strcmp(table_name, "users") == 0) ? "user" : 
             (strcmp(table_name, "companies") == 0) ? "company" : "transaction",
             table_name);
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        strcpy(id, prefix);
        strcat(id, "1");
        return id;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        const char* existing_id = (const char*)sqlite3_column_text(stmt, 0);
        if (existing_id) {
            // Extract number from ID (e.g., "U1" -> 1, "C5" -> 5)
            int num = 0;
            sscanf(existing_id, "%*[^0-9]%d", &num);
            if (num > max_num) {
                max_num = num;
            }
        }
    }
    
    sqlite3_finalize(stmt);
    
    max_num++;
    snprintf(id, 20, "%s%d", prefix, max_num);
    return id;
}

// ============ USER CRUD OPERATIONS ============

int create_user(sqlite3* db, const char* firstname, const char* lastname, 
                const char* date_of_birth, const char* address, double balance, User* user) {
    char* user_id = get_next_id(db, "users", "U");
    char sql[1000];
    char* err_msg = 0;
    
    snprintf(sql, sizeof(sql),
        "INSERT INTO users (user_id, firstname, lastname, date_of_birth, address, balance) "
        "VALUES ('%s', '%s', '%s', '%s', '%s', %.2f)",
        user_id, firstname, lastname, date_of_birth, address, balance);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        free(user_id);
        return 1;
    }
    
    if (user) {
        strcpy(user->user_id, user_id);
        strcpy(user->firstname, firstname);
        strcpy(user->lastname, lastname);
        strcpy(user->date_of_birth, date_of_birth);
        strcpy(user->address, address);
        user->balance = balance;
    }
    
    free(user_id);
    return 0;
}

int get_user(sqlite3* db, const char* user_id, User* user) {
    char sql[200];
    sqlite3_stmt* stmt;
    
    snprintf(sql, sizeof(sql), "SELECT user_id, firstname, lastname, date_of_birth, address, balance "
                                "FROM users WHERE user_id = '%s'", user_id);
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        strcpy(user->user_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy(user->firstname, (const char*)sqlite3_column_text(stmt, 1));
        strcpy(user->lastname, (const char*)sqlite3_column_text(stmt, 2));
        strcpy(user->date_of_birth, (const char*)sqlite3_column_text(stmt, 3));
        strcpy(user->address, (const char*)sqlite3_column_text(stmt, 4));
        user->balance = sqlite3_column_double(stmt, 5);
        sqlite3_finalize(stmt);
        return 0;
    }
    
    sqlite3_finalize(stmt);
    return 1;
}

int get_all_users(sqlite3* db, User** users, int* count) {
    const char* sql = "SELECT user_id, firstname, lastname, date_of_birth, address, balance FROM users";
    sqlite3_stmt* stmt;
    *count = 0;
    int capacity = 10;
    *users = (User*)malloc(capacity * sizeof(User));
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        if (*count >= capacity) {
            capacity *= 2;
            *users = (User*)realloc(*users, capacity * sizeof(User));
        }
        
        strcpy((*users)[*count].user_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy((*users)[*count].firstname, (const char*)sqlite3_column_text(stmt, 1));
        strcpy((*users)[*count].lastname, (const char*)sqlite3_column_text(stmt, 2));
        strcpy((*users)[*count].date_of_birth, (const char*)sqlite3_column_text(stmt, 3));
        strcpy((*users)[*count].address, (const char*)sqlite3_column_text(stmt, 4));
        (*users)[*count].balance = sqlite3_column_double(stmt, 5);
        (*count)++;
    }
    
    sqlite3_finalize(stmt);
    return 0;
}

int update_user(sqlite3* db, const char* user_id, const char* firstname, 
                const char* lastname, const char* date_of_birth, 
                const char* address, double balance) {
    char sql[2000];
    char* err_msg = 0;
    int has_update = 0;
    
    strcpy(sql, "UPDATE users SET ");
    
    if (firstname) {
        if (has_update) strcat(sql, ", ");
        char temp[300];
        snprintf(temp, sizeof(temp), "firstname = '%s'", firstname);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (lastname) {
        if (has_update) strcat(sql, ", ");
        char temp[300];
        snprintf(temp, sizeof(temp), "lastname = '%s'", lastname);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (date_of_birth) {
        if (has_update) strcat(sql, ", ");
        char temp[300];
        snprintf(temp, sizeof(temp), "date_of_birth = '%s'", date_of_birth);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (address) {
        if (has_update) strcat(sql, ", ");
        char temp[600];
        snprintf(temp, sizeof(temp), "address = '%s'", address);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (balance != -999999.0) {  // Use sentinel value to indicate no update
        if (has_update) strcat(sql, ", ");
        char temp[100];
        snprintf(temp, sizeof(temp), "balance = %.2f", balance);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (!has_update) {
        return 1;  // No fields to update
    }
    
    char where[100];
    snprintf(where, sizeof(where), " WHERE user_id = '%s'", user_id);
    strcat(sql, where);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}

int delete_user(sqlite3* db, const char* user_id) {
    char sql[500];
    char* err_msg = 0;
    
    // First delete related transactions
    snprintf(sql, sizeof(sql), "DELETE FROM transactions WHERE user_id = '%s'", user_id);
    sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (err_msg) {
        sqlite3_free(err_msg);
        err_msg = 0;
    }
    
    // Then delete user
    snprintf(sql, sizeof(sql), "DELETE FROM users WHERE user_id = '%s'", user_id);
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}

// ============ COMPANY CRUD OPERATIONS ============

int create_company(sqlite3* db, const char* name, const char* location, Company* company) {
    char* company_id = get_next_id(db, "companies", "C");
    char sql[1000];
    char* err_msg = 0;
    
    snprintf(sql, sizeof(sql),
        "INSERT INTO companies (company_id, name, location) "
        "VALUES ('%s', '%s', '%s')",
        company_id, name, location);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        free(company_id);
        return 1;
    }
    
    if (company) {
        strcpy(company->company_id, company_id);
        strcpy(company->name, name);
        strcpy(company->location, location);
    }
    
    free(company_id);
    return 0;
}

int get_company(sqlite3* db, const char* company_id, Company* company) {
    char sql[200];
    sqlite3_stmt* stmt;
    
    snprintf(sql, sizeof(sql), "SELECT company_id, name, location FROM companies WHERE company_id = '%s'", company_id);
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        strcpy(company->company_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy(company->name, (const char*)sqlite3_column_text(stmt, 1));
        strcpy(company->location, (const char*)sqlite3_column_text(stmt, 2));
        sqlite3_finalize(stmt);
        return 0;
    }
    
    sqlite3_finalize(stmt);
    return 1;
}

int get_all_companies(sqlite3* db, Company** companies, int* count) {
    const char* sql = "SELECT company_id, name, location FROM companies";
    sqlite3_stmt* stmt;
    *count = 0;
    int capacity = 10;
    *companies = (Company*)malloc(capacity * sizeof(Company));
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        if (*count >= capacity) {
            capacity *= 2;
            *companies = (Company*)realloc(*companies, capacity * sizeof(Company));
        }
        
        strcpy((*companies)[*count].company_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy((*companies)[*count].name, (const char*)sqlite3_column_text(stmt, 1));
        strcpy((*companies)[*count].location, (const char*)sqlite3_column_text(stmt, 2));
        (*count)++;
    }
    
    sqlite3_finalize(stmt);
    return 0;
}

int update_company(sqlite3* db, const char* company_id, const char* name, const char* location) {
    char sql[1000];
    char* err_msg = 0;
    int has_update = 0;
    
    strcpy(sql, "UPDATE companies SET ");
    
    if (name) {
        char temp[300];
        snprintf(temp, sizeof(temp), "name = '%s'", name);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (location) {
        if (has_update) strcat(sql, ", ");
        char temp[300];
        snprintf(temp, sizeof(temp), "location = '%s'", location);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (!has_update) {
        return 1;
    }
    
    char where[100];
    snprintf(where, sizeof(where), " WHERE company_id = '%s'", company_id);
    strcat(sql, where);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}

int delete_company(sqlite3* db, const char* company_id) {
    char sql[500];
    char* err_msg = 0;
    
    // First delete related transactions
    snprintf(sql, sizeof(sql), "DELETE FROM transactions WHERE company_id = '%s'", company_id);
    sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (err_msg) {
        sqlite3_free(err_msg);
        err_msg = 0;
    }
    
    // Then delete company
    snprintf(sql, sizeof(sql), "DELETE FROM companies WHERE company_id = '%s'", company_id);
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}

// ============ TRANSACTION CRUD OPERATIONS ============

int create_transaction(sqlite3* db, const char* user_id, const char* company_id,
                       int number_of_shares, const char* transaction_datetime, Transaction* transaction) {
    char* transaction_id = get_next_id(db, "transactions", "T");
    char sql[1000];
    char* err_msg = 0;
    char datetime[20];
    
    if (transaction_datetime && strlen(transaction_datetime) > 0) {
        strcpy(datetime, transaction_datetime);
    } else {
        // Get current datetime
        time_t now = time(NULL);
        struct tm* t = localtime(&now);
        snprintf(datetime, sizeof(datetime), "%04d-%02d-%02d %02d:%02d:%02d",
                 t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
                 t->tm_hour, t->tm_min, t->tm_sec);
    }
    
    snprintf(sql, sizeof(sql),
        "INSERT INTO transactions (transaction_id, user_id, company_id, number_of_shares, transaction_datetime) "
        "VALUES ('%s', '%s', '%s', %d, '%s')",
        transaction_id, user_id, company_id, number_of_shares, datetime);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        free(transaction_id);
        return 1;
    }
    
    if (transaction) {
        strcpy(transaction->transaction_id, transaction_id);
        strcpy(transaction->user_id, user_id);
        strcpy(transaction->company_id, company_id);
        transaction->number_of_shares = number_of_shares;
        strcpy(transaction->transaction_datetime, datetime);
    }
    
    free(transaction_id);
    return 0;
}

int get_transaction(sqlite3* db, const char* transaction_id, Transaction* transaction) {
    char sql[200];
    sqlite3_stmt* stmt;
    
    snprintf(sql, sizeof(sql), 
        "SELECT transaction_id, user_id, company_id, number_of_shares, transaction_datetime "
        "FROM transactions WHERE transaction_id = '%s'", transaction_id);
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        strcpy(transaction->transaction_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy(transaction->user_id, (const char*)sqlite3_column_text(stmt, 1));
        strcpy(transaction->company_id, (const char*)sqlite3_column_text(stmt, 2));
        transaction->number_of_shares = sqlite3_column_int(stmt, 3);
        strcpy(transaction->transaction_datetime, (const char*)sqlite3_column_text(stmt, 4));
        sqlite3_finalize(stmt);
        return 0;
    }
    
    sqlite3_finalize(stmt);
    return 1;
}

int get_all_transactions(sqlite3* db, Transaction** transactions, int* count) {
    const char* sql = "SELECT transaction_id, user_id, company_id, number_of_shares, transaction_datetime FROM transactions";
    sqlite3_stmt* stmt;
    *count = 0;
    int capacity = 10;
    *transactions = (Transaction*)malloc(capacity * sizeof(Transaction));
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        if (*count >= capacity) {
            capacity *= 2;
            *transactions = (Transaction*)realloc(*transactions, capacity * sizeof(Transaction));
        }
        
        strcpy((*transactions)[*count].transaction_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy((*transactions)[*count].user_id, (const char*)sqlite3_column_text(stmt, 1));
        strcpy((*transactions)[*count].company_id, (const char*)sqlite3_column_text(stmt, 2));
        (*transactions)[*count].number_of_shares = sqlite3_column_int(stmt, 3);
        strcpy((*transactions)[*count].transaction_datetime, (const char*)sqlite3_column_text(stmt, 4));
        (*count)++;
    }
    
    sqlite3_finalize(stmt);
    return 0;
}

int get_transactions_by_user(sqlite3* db, const char* user_id, Transaction** transactions, int* count) {
    char sql[200];
    sqlite3_stmt* stmt;
    *count = 0;
    int capacity = 10;
    *transactions = (Transaction*)malloc(capacity * sizeof(Transaction));
    
    snprintf(sql, sizeof(sql), 
        "SELECT transaction_id, user_id, company_id, number_of_shares, transaction_datetime "
        "FROM transactions WHERE user_id = '%s'", user_id);
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        if (*count >= capacity) {
            capacity *= 2;
            *transactions = (Transaction*)realloc(*transactions, capacity * sizeof(Transaction));
        }
        
        strcpy((*transactions)[*count].transaction_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy((*transactions)[*count].user_id, (const char*)sqlite3_column_text(stmt, 1));
        strcpy((*transactions)[*count].company_id, (const char*)sqlite3_column_text(stmt, 2));
        (*transactions)[*count].number_of_shares = sqlite3_column_int(stmt, 3);
        strcpy((*transactions)[*count].transaction_datetime, (const char*)sqlite3_column_text(stmt, 4));
        (*count)++;
    }
    
    sqlite3_finalize(stmt);
    return 0;
}

int get_transactions_by_company(sqlite3* db, const char* company_id, Transaction** transactions, int* count) {
    char sql[200];
    sqlite3_stmt* stmt;
    *count = 0;
    int capacity = 10;
    *transactions = (Transaction*)malloc(capacity * sizeof(Transaction));
    
    snprintf(sql, sizeof(sql), 
        "SELECT transaction_id, user_id, company_id, number_of_shares, transaction_datetime "
        "FROM transactions WHERE company_id = '%s'", company_id);
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return 1;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        if (*count >= capacity) {
            capacity *= 2;
            *transactions = (Transaction*)realloc(*transactions, capacity * sizeof(Transaction));
        }
        
        strcpy((*transactions)[*count].transaction_id, (const char*)sqlite3_column_text(stmt, 0));
        strcpy((*transactions)[*count].user_id, (const char*)sqlite3_column_text(stmt, 1));
        strcpy((*transactions)[*count].company_id, (const char*)sqlite3_column_text(stmt, 2));
        (*transactions)[*count].number_of_shares = sqlite3_column_int(stmt, 3);
        strcpy((*transactions)[*count].transaction_datetime, (const char*)sqlite3_column_text(stmt, 4));
        (*count)++;
    }
    
    sqlite3_finalize(stmt);
    return 0;
}

int update_transaction(sqlite3* db, const char* transaction_id, const char* user_id,
                      const char* company_id, int number_of_shares, const char* transaction_datetime) {
    char sql[2000];
    char* err_msg = 0;
    int has_update = 0;
    
    strcpy(sql, "UPDATE transactions SET ");
    
    if (user_id) {
        char temp[300];
        snprintf(temp, sizeof(temp), "user_id = '%s'", user_id);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (company_id) {
        if (has_update) strcat(sql, ", ");
        char temp[300];
        snprintf(temp, sizeof(temp), "company_id = '%s'", company_id);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (number_of_shares != -999999) {  // Sentinel value
        if (has_update) strcat(sql, ", ");
        char temp[100];
        snprintf(temp, sizeof(temp), "number_of_shares = %d", number_of_shares);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (transaction_datetime) {
        if (has_update) strcat(sql, ", ");
        char temp[300];
        snprintf(temp, sizeof(temp), "transaction_datetime = '%s'", transaction_datetime);
        strcat(sql, temp);
        has_update = 1;
    }
    
    if (!has_update) {
        return 1;
    }
    
    char where[100];
    snprintf(where, sizeof(where), " WHERE transaction_id = '%s'", transaction_id);
    strcat(sql, where);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}

int delete_transaction(sqlite3* db, const char* transaction_id) {
    char sql[200];
    char* err_msg = 0;
    
    snprintf(sql, sizeof(sql), "DELETE FROM transactions WHERE transaction_id = '%s'", transaction_id);
    int rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return 1;
    }
    
    return 0;
}

