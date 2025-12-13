from sqlalchemy.orm import Session
from models import User, Company, Transaction
from datetime import date, datetime
from decimal import Decimal
import re

# Helper function to get next ID
def get_next_id(db: Session, model_class, prefix: str):
    """Get the next available ID (e.g., U1, C1, T1...)"""
    # Get all existing IDs
    existing_ids = db.query(model_class).all()
    
    if not existing_ids:
        return f"{prefix}1"
    
    # Extract numbers from existing IDs
    numbers = []
    for item in existing_ids:
        if model_class == User:
            id_value = item.user_id
        elif model_class == Company:
            id_value = item.company_id
        elif model_class == Transaction:
            id_value = item.transaction_id
        else:
            continue
        
        # Convert to string if it's not already
        if not isinstance(id_value, str):
            id_value = str(id_value)
        
        match = re.search(r'\d+$', id_value)
        if match:
            numbers.append(int(match.group()))
    
    if not numbers:
        return f"{prefix}1"
    
    next_number = max(numbers) + 1
    return f"{prefix}{next_number}"


# ============ USER CRUD OPERATIONS ============

def create_user(db: Session, firstname: str, lastname: str, date_of_birth: date, 
                address: str, balance: Decimal = Decimal('0.00')):
    """Create a new user"""
    user_id = get_next_id(db, User, "U")
    user = User(
        user_id=user_id,
        firstname=firstname,
        lastname=lastname,
        date_of_birth=date_of_birth,
        address=address,
        balance=balance
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str):
    """Get a user by ID"""
    return db.query(User).filter(User.user_id == user_id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, firstname: str = None, lastname: str = None,
                date_of_birth: date = None, address: str = None, balance: Decimal = None):
    """Update a user"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    
    if firstname is not None:
        user.firstname = firstname
    if lastname is not None:
        user.lastname = lastname
    if date_of_birth is not None:
        user.date_of_birth = date_of_birth
    if address is not None:
        user.address = address
    if balance is not None:
        user.balance = balance
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str):
    """Delete a user and all related transactions"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return False
    
    # Delete all transactions related to this user first
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    for transaction in transactions:
        db.delete(transaction)
    
    db.delete(user)
    db.commit()
    return True


# ============ COMPANY CRUD OPERATIONS ============

def create_company(db: Session, name: str, location: str):
    """Create a new company"""
    company_id = get_next_id(db, Company, "C")
    company = Company(
        company_id=company_id,
        name=name,
        location=location
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company(db: Session, company_id: str):
    """Get a company by ID"""
    return db.query(Company).filter(Company.company_id == company_id).first()


def get_all_companies(db: Session, skip: int = 0, limit: int = 100):
    """Get all companies"""
    return db.query(Company).offset(skip).limit(limit).all()


def update_company(db: Session, company_id: str, name: str = None, location: str = None):
    """Update a company"""
    company = db.query(Company).filter(Company.company_id == company_id).first()
    if not company:
        return None
    
    if name is not None:
        company.name = name
    if location is not None:
        company.location = location
    
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: str):
    """Delete a company and all related transactions"""
    company = db.query(Company).filter(Company.company_id == company_id).first()
    if not company:
        return False
    
    # Delete all transactions related to this company first
    transactions = db.query(Transaction).filter(Transaction.company_id == company_id).all()
    for transaction in transactions:
        db.delete(transaction)
    
    db.delete(company)
    db.commit()
    return True


# ============ TRANSACTION CRUD OPERATIONS ============

def create_transaction(db: Session, user_id: str, company_id: str, 
                       number_of_shares: int, transaction_datetime: datetime = None):
    """Create a new transaction"""
    if transaction_datetime is None:
        transaction_datetime = datetime.utcnow()
    
    transaction_id = get_next_id(db, Transaction, "T")
    transaction = Transaction(
        transaction_id=transaction_id,
        user_id=user_id,
        company_id=company_id,
        number_of_shares=number_of_shares,
        transaction_datetime=transaction_datetime
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transaction(db: Session, transaction_id: str):
    """Get a transaction by ID"""
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()


def get_all_transactions(db: Session, skip: int = 0, limit: int = 100):
    """Get all transactions"""
    return db.query(Transaction).offset(skip).limit(limit).all()


def get_transactions_by_user(db: Session, user_id: str):
    """Get all transactions for a specific user"""
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


def get_transactions_by_company(db: Session, company_id: str):
    """Get all transactions for a specific company"""
    return db.query(Transaction).filter(Transaction.company_id == company_id).all()


def get_transactions_by_user_and_company(db: Session, user_id: str, company_id: str):
    """Get all transactions for a specific user and company"""
    return db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.company_id == company_id
    ).all()


def update_transaction(db: Session, transaction_id: str, user_id: str = None, 
                      company_id: str = None, number_of_shares: int = None,
                      transaction_datetime: datetime = None):
    """Update a transaction"""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        return None
    
    if user_id is not None:
        transaction.user_id = user_id
    if company_id is not None:
        transaction.company_id = company_id
    if number_of_shares is not None:
        transaction.number_of_shares = number_of_shares
    if transaction_datetime is not None:
        transaction.transaction_datetime = transaction_datetime
    
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction_id: str):
    """Delete a transaction"""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        return False
    
    db.delete(transaction)
    db.commit()
    return True

