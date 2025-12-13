#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "database.h"
#include "crud.h"
#include "models.h"

void print_user(User* user) {
    printf("  %s: %s %s, DOB: %s, Address: %s, Balance: $%.2f\n",
           user->user_id, user->firstname, user->lastname,
           user->date_of_birth, user->address, user->balance);
}

void print_company(Company* company) {
    printf("  %s: %s, Location: %s\n",
           company->company_id, company->name, company->location);
}

void print_transaction(Transaction* trans) {
    printf("  Transaction %s: User %s -> Company %s, Shares: %d, DateTime: %s\n",
           trans->transaction_id, trans->user_id, trans->company_id,
           trans->number_of_shares, trans->transaction_datetime);
}

int main() {
    sqlite3* db = db_connect("app.db");
    if (!db) {
        return 1;
    }
    
    if (db_init(db) != 0) {
        db_close(db);
        return 1;
    }
    
    printf("Database initialized successfully!\n");
    printf("==================================================\n");
    printf("USER CRUD OPERATIONS\n");
    printf("==================================================\n\n");
    
    // CREATE - Add users
    printf("1. Creating users...\n");
    User user1, user2;
    create_user(db, "John", "Doe", "1990-05-15", "123 Main St, New York, NY", 1500.50, &user1);
    printf("Created user: %s - %s %s\n", user1.user_id, user1.firstname, user1.lastname);
    
    create_user(db, "Jane", "Smith", "1985-08-22", "456 Oak Ave, Los Angeles, CA", 2500.75, &user2);
    printf("Created user: %s - %s %s\n", user2.user_id, user2.firstname, user2.lastname);
    
    // READ - Get all users
    printf("\n2. Reading all users...\n");
    User* users;
    int user_count;
    get_all_users(db, &users, &user_count);
    for (int i = 0; i < user_count; i++) {
        print_user(&users[i]);
    }
    free(users);
    
    // READ - Get single user
    printf("\n3. Reading single user (U1)...\n");
    User user;
    if (get_user(db, "U1", &user) == 0) {
        printf("  Found: %s %s, Balance: $%.2f\n", user.firstname, user.lastname, user.balance);
    }
    
    // UPDATE - Update user
    printf("\n4. Updating user U1...\n");
    update_user(db, "U1", NULL, NULL, NULL, "789 Pine Rd, Boston, MA", 2000.00);
    if (get_user(db, "U1", &user) == 0) {
        printf("  Updated: %s %s, New Balance: $%.2f, New Address: %s\n",
               user.firstname, user.lastname, user.balance, user.address);
    }
    
    printf("\n==================================================\n");
    printf("COMPANY CRUD OPERATIONS\n");
    printf("==================================================\n\n");
    
    // CREATE - Add companies
    printf("1. Creating companies...\n");
    Company company1, company2;
    create_company(db, "Tech Solutions Inc", "San Francisco, CA", &company1);
    printf("Created company: %s - %s\n", company1.company_id, company1.name);
    
    create_company(db, "Global Industries Ltd", "New York, NY", &company2);
    printf("Created company: %s - %s\n", company2.company_id, company2.name);
    
    // READ - Get all companies
    printf("\n2. Reading all companies...\n");
    Company* companies;
    int company_count;
    get_all_companies(db, &companies, &company_count);
    for (int i = 0; i < company_count; i++) {
        print_company(&companies[i]);
    }
    free(companies);
    
    // READ - Get single company
    printf("\n3. Reading single company (C1)...\n");
    Company company;
    if (get_company(db, "C1", &company) == 0) {
        printf("  Found: %s, Location: %s\n", company.name, company.location);
    }
    
    // UPDATE - Update company
    printf("\n4. Updating company C1...\n");
    update_company(db, "C1", NULL, "Seattle, WA");
    if (get_company(db, "C1", &company) == 0) {
        printf("  Updated: %s, New Location: %s\n", company.name, company.location);
    }
    
    printf("\n==================================================\n");
    printf("TRANSACTION CRUD OPERATIONS\n");
    printf("==================================================\n\n");
    
    // CREATE - Add transactions
    printf("1. Creating transactions...\n");
    Transaction trans1, trans2, trans3;
    create_transaction(db, "U1", "C1", 100, "2024-01-15 10:30:00", &trans1);
    printf("Created transaction: ID %s, User %s, Company %s, Shares: %d\n",
           trans1.transaction_id, trans1.user_id, trans1.company_id, trans1.number_of_shares);
    
    create_transaction(db, "U1", "C2", 50, NULL, &trans2);
    printf("Created transaction: ID %s, User %s, Company %s, Shares: %d\n",
           trans2.transaction_id, trans2.user_id, trans2.company_id, trans2.number_of_shares);
    
    create_transaction(db, "U2", "C1", 200, "2024-01-16 14:45:00", &trans3);
    printf("Created transaction: ID %s, User %s, Company %s, Shares: %d\n",
           trans3.transaction_id, trans3.user_id, trans3.company_id, trans3.number_of_shares);
    
    // READ - Get all transactions
    printf("\n2. Reading all transactions...\n");
    Transaction* transactions;
    int trans_count;
    get_all_transactions(db, &transactions, &trans_count);
    for (int i = 0; i < trans_count; i++) {
        print_transaction(&transactions[i]);
    }
    free(transactions);
    
    // READ - Get single transaction
    printf("\n3. Reading single transaction (T1)...\n");
    Transaction trans;
    if (get_transaction(db, "T1", &trans) == 0) {
        printf("  Found: User %s, Company %s, Shares: %d\n",
               trans.user_id, trans.company_id, trans.number_of_shares);
    }
    
    // UPDATE - Update transaction
    printf("\n4. Updating transaction T1...\n");
    update_transaction(db, "T1", NULL, NULL, 150, NULL);
    if (get_transaction(db, "T1", &trans) == 0) {
        printf("  Updated: Shares changed to %d\n", trans.number_of_shares);
    }
    
    printf("\n==================================================\n");
    printf("Final State\n");
    printf("==================================================\n\n");
    
    printf("All Users:\n");
    get_all_users(db, &users, &user_count);
    for (int i = 0; i < user_count; i++) {
        printf("  %s: %s %s, Balance: $%.2f\n",
               users[i].user_id, users[i].firstname, users[i].lastname, users[i].balance);
    }
    free(users);
    
    printf("\nAll Companies:\n");
    get_all_companies(db, &companies, &company_count);
    for (int i = 0; i < company_count; i++) {
        printf("  %s: %s, Location: %s\n",
               companies[i].company_id, companies[i].name, companies[i].location);
    }
    free(companies);
    
    printf("\nAll Transactions:\n");
    get_all_transactions(db, &transactions, &trans_count);
    for (int i = 0; i < trans_count; i++) {
        print_transaction(&transactions[i]);
    }
    free(transactions);
    
    db_close(db);
    return 0;
}


