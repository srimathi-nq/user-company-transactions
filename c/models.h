#ifndef MODELS_H
#define MODELS_H

#include <time.h>

// User structure
typedef struct {
    char user_id[20];
    char firstname[100];
    char lastname[100];
    char date_of_birth[11];  // YYYY-MM-DD format
    char address[500];
    double balance;
} User;

// Company structure
typedef struct {
    char company_id[20];
    char name[200];
    char location[200];
} Company;

// Transaction structure
typedef struct {
    char transaction_id[20];
    char user_id[20];
    char company_id[20];
    int number_of_shares;
    char transaction_datetime[20];  // YYYY-MM-DD HH:MM:SS format
} Transaction;

#endif // MODELS_H


