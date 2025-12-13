from database import engine, SessionLocal
from models import Base, User, Company, Transaction
from crud import (
    create_user, get_user, get_all_users, update_user, delete_user,
    create_company, get_company, get_all_companies, update_company, delete_company,
    create_transaction, get_transaction, get_all_transactions, 
    get_transactions_by_user, get_transactions_by_company,
    get_transactions_by_user_and_company, update_transaction, delete_transaction
)
from datetime import date, datetime
from decimal import Decimal

# Create all tables
def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def main():
    # Initialize database
    init_db()
    
    # Create a database session
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("USER CRUD OPERATIONS")
        print("=" * 50)
        
        # CREATE - Add users
        print("\n1. Creating users...")
        user1 = create_user(
            db=db,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 5, 15),
            address="123 Main St, New York, NY",
            balance=Decimal('1500.50')
        )
        print(f"Created user: {user1.user_id} - {user1.firstname} {user1.lastname}")
        
        user2 = create_user(
            db=db,
            firstname="Jane",
            lastname="Smith",
            date_of_birth=date(1985, 8, 22),
            address="456 Oak Ave, Los Angeles, CA",
            balance=Decimal('2500.75')
        )
        print(f"Created user: {user2.user_id} - {user2.firstname} {user2.lastname}")
        
        # READ - Get all users
        print("\n2. Reading all users...")
        users = get_all_users(db)
        for user in users:
            print(f"  {user.user_id}: {user.firstname} {user.lastname}, DOB: {user.date_of_birth}, "
                  f"Address: {user.address}, Balance: ${user.balance}")
        
        # READ - Get single user
        print("\n3. Reading single user (U1)...")
        user = get_user(db, "U1")
        if user:
            print(f"  Found: {user.firstname} {user.lastname}, Balance: ${user.balance}")
        
        # UPDATE - Update user
        print("\n4. Updating user U1...")
        updated_user = update_user(
            db=db,
            user_id="U1",
            balance=Decimal('2000.00'),
            address="789 Pine Rd, Boston, MA"
        )
        if updated_user:
            print(f"  Updated: {updated_user.firstname} {updated_user.lastname}, "
                  f"New Balance: ${updated_user.balance}, New Address: {updated_user.address}")
        
        print("\n" + "=" * 50)
        print("COMPANY CRUD OPERATIONS")
        print("=" * 50)
        
        # CREATE - Add companies
        print("\n1. Creating companies...")
        company1 = create_company(
            db=db,
            name="Tech Solutions Inc",
            location="San Francisco, CA"
        )
        print(f"Created company: {company1.company_id} - {company1.name}")
        
        company2 = create_company(
            db=db,
            name="Global Industries Ltd",
            location="New York, NY"
        )
        print(f"Created company: {company2.company_id} - {company2.name}")
        
        # READ - Get all companies
        print("\n2. Reading all companies...")
        companies = get_all_companies(db)
        for company in companies:
            print(f"  {company.company_id}: {company.name}, Location: {company.location}")
        
        # READ - Get single company
        print("\n3. Reading single company (C1)...")
        company = get_company(db, "C1")
        if company:
            print(f"  Found: {company.name}, Location: {company.location}")
        
        # UPDATE - Update company
        print("\n4. Updating company C1...")
        updated_company = update_company(
            db=db,
            company_id="C1",
            location="Seattle, WA"
        )
        if updated_company:
            print(f"  Updated: {updated_company.name}, New Location: {updated_company.location}")
        
        print("\n" + "=" * 50)
        print("TRANSACTION CRUD OPERATIONS")
        print("=" * 50)
        
        # CREATE - Add transactions
        print("\n1. Creating transactions...")
        transaction1 = create_transaction(
            db=db,
            user_id="U1",
            company_id="C1",
            number_of_shares=100,
            transaction_datetime=datetime(2024, 1, 15, 10, 30, 0)
        )
        print(f"Created transaction: ID {transaction1.transaction_id}, User {transaction1.user_id}, "
              f"Company {transaction1.company_id}, Shares: {transaction1.number_of_shares}, "
              f"DateTime: {transaction1.transaction_datetime}")
        
        transaction2 = create_transaction(
            db=db,
            user_id="U1",
            company_id="C2",
            number_of_shares=50
        )
        print(f"Created transaction: ID {transaction2.transaction_id}, User {transaction2.user_id}, "
              f"Company {transaction2.company_id}, Shares: {transaction2.number_of_shares}, "
              f"DateTime: {transaction2.transaction_datetime}")
        
        transaction3 = create_transaction(
            db=db,
            user_id="U2",
            company_id="C1",
            number_of_shares=200,
            transaction_datetime=datetime(2024, 1, 16, 14, 45, 0)
        )
        print(f"Created transaction: ID {transaction3.transaction_id}, User {transaction3.user_id}, "
              f"Company {transaction3.company_id}, Shares: {transaction3.number_of_shares}, "
              f"DateTime: {transaction3.transaction_datetime}")
        
        # READ - Get all transactions
        print("\n2. Reading all transactions...")
        transactions = get_all_transactions(db)
        for trans in transactions:
            print(f"  Transaction {trans.transaction_id}: User {trans.user_id} -> Company {trans.company_id}, "
                  f"Shares: {trans.number_of_shares}, DateTime: {trans.transaction_datetime}")
        
        # READ - Get single transaction
        print("\n3. Reading single transaction (ID: T1)...")
        transaction = get_transaction(db, "T1")
        if transaction:
            print(f"  Found: User {transaction.user_id}, Company {transaction.company_id}, "
                  f"Shares: {transaction.number_of_shares}")
        
        # READ - Get transactions by user
        print("\n4. Reading transactions for user U1...")
        user_transactions = get_transactions_by_user(db, "U1")
        for trans in user_transactions:
            print(f"  Transaction {trans.transaction_id}: Company {trans.company_id}, "
                  f"Shares: {trans.number_of_shares}")
        
        # READ - Get transactions by company
        print("\n5. Reading transactions for company C1...")
        company_transactions = get_transactions_by_company(db, "C1")
        for trans in company_transactions:
            print(f"  Transaction {trans.transaction_id}: User {trans.user_id}, "
                  f"Shares: {trans.number_of_shares}")
        
        # UPDATE - Update transaction
        print("\n6. Updating transaction T1...")
        updated_transaction = update_transaction(
            db=db,
            transaction_id="T1",
            number_of_shares=150
        )
        if updated_transaction:
            print(f"  Updated: Shares changed to {updated_transaction.number_of_shares}")
        
        # DELETE - Delete operations (commented out to keep data for demonstration)
        # Uncomment to test delete operations
        # print("\n7. Deleting transaction ID 3...")
        # if delete_transaction(db, 3):
        #     print("  Transaction 3 deleted successfully")
        
        print("\n" + "=" * 50)
        print("Final State")
        print("=" * 50)
        
        print("\nAll Users:")
        users = get_all_users(db)
        for user in users:
            print(f"  {user.user_id}: {user.firstname} {user.lastname}, Balance: ${user.balance}")
        
        print("\nAll Companies:")
        companies = get_all_companies(db)
        for company in companies:
            print(f"  {company.company_id}: {company.name}, Location: {company.location}")
        
        print("\nAll Transactions:")
        transactions = get_all_transactions(db)
        for trans in transactions:
            print(f"  Transaction {trans.transaction_id}: User {trans.user_id} -> Company {trans.company_id}, "
                  f"Shares: {trans.number_of_shares}, DateTime: {trans.transaction_datetime}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

