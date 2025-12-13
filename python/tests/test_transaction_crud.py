import pytest
from datetime import date, datetime
from crud import (
    create_transaction, get_transaction, get_all_transactions,
    get_transactions_by_user, get_transactions_by_company,
    get_transactions_by_user_and_company, update_transaction, delete_transaction,
    create_user, create_company
)


class TestTransactionCreate:
    """Test cases for creating transactions"""
    
    def test_create_transaction_basic(self, db_session):
        """Test creating a basic transaction"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db=db_session,
            user_id=user.user_id,
            company_id=company.company_id,
            number_of_shares=100
        )
        
        assert transaction.transaction_id == "T1"
        assert transaction.user_id == user.user_id
        assert transaction.company_id == company.company_id
        assert transaction.number_of_shares == 100
        assert transaction.transaction_datetime is not None
    
    def test_create_transaction_with_datetime(self, db_session):
        """Test creating a transaction with specific datetime"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        trans_datetime = datetime(2024, 1, 15, 10, 30, 0)
        transaction = create_transaction(
            db=db_session,
            user_id=user.user_id,
            company_id=company.company_id,
            number_of_shares=50,
            transaction_datetime=trans_datetime
        )
        
        assert transaction.transaction_datetime == trans_datetime
    
    def test_create_transaction_zero_shares(self, db_session):
        """Test creating a transaction with zero shares (edge case)"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db=db_session,
            user_id=user.user_id,
            company_id=company.company_id,
            number_of_shares=0
        )
        
        assert transaction.number_of_shares == 0
    
    def test_create_transaction_large_shares(self, db_session):
        """Test creating a transaction with very large number of shares"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db=db_session,
            user_id=user.user_id,
            company_id=company.company_id,
            number_of_shares=1000000
        )
        
        assert transaction.number_of_shares == 1000000
    
    def test_create_transaction_negative_shares(self, db_session):
        """Test creating a transaction with negative shares (edge case - should work)"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db=db_session,
            user_id=user.user_id,
            company_id=company.company_id,
            number_of_shares=-50
        )
        
        assert transaction.number_of_shares == -50
    
    def test_create_multiple_transactions_auto_id(self, db_session):
        """Test that transaction IDs are auto-incremented"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        trans1 = create_transaction(db_session, user.user_id, company.company_id, 100)
        trans2 = create_transaction(db_session, user.user_id, company.company_id, 200)
        trans3 = create_transaction(db_session, user.user_id, company.company_id, 300)
        
        assert trans1.transaction_id == "T1"
        assert trans2.transaction_id == "T2"
        assert trans3.transaction_id == "T3"
    
    def test_create_transaction_multiple_users_same_company(self, db_session):
        """Test creating transactions for multiple users with same company"""
        user1 = create_user(db_session, "User1", "Test", date(1990, 1, 1), "Addr1")
        user2 = create_user(db_session, "User2", "Test", date(1991, 1, 1), "Addr2")
        company = create_company(db_session, "Tech Corp", "Location")
        
        trans1 = create_transaction(db_session, user1.user_id, company.company_id, 100)
        trans2 = create_transaction(db_session, user2.user_id, company.company_id, 200)
        
        assert trans1.user_id == user1.user_id
        assert trans2.user_id == user2.user_id
        assert trans1.company_id == company.company_id
        assert trans2.company_id == company.company_id
    
    def test_create_transaction_same_user_multiple_companies(self, db_session):
        """Test creating transactions for same user with multiple companies"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company1 = create_company(db_session, "Company1", "Loc1")
        company2 = create_company(db_session, "Company2", "Loc2")
        
        trans1 = create_transaction(db_session, user.user_id, company1.company_id, 100)
        trans2 = create_transaction(db_session, user.user_id, company2.company_id, 200)
        
        assert trans1.user_id == user.user_id
        assert trans2.user_id == user.user_id
        assert trans1.company_id == company1.company_id
        assert trans2.company_id == company2.company_id


class TestTransactionRead:
    """Test cases for reading transactions"""
    
    def test_get_transaction_existing(self, db_session):
        """Test getting an existing transaction"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        created = create_transaction(db_session, user.user_id, company.company_id, 100)
        
        transaction = get_transaction(db_session, created.transaction_id)
        
        assert transaction is not None
        assert transaction.transaction_id == created.transaction_id
        assert transaction.number_of_shares == 100
    
    def test_get_transaction_nonexistent(self, db_session):
        """Test getting a non-existent transaction"""
        transaction = get_transaction(db_session, "T999")
        assert transaction is None
    
    def test_get_all_transactions_empty(self, db_session):
        """Test getting all transactions when none exist"""
        transactions = get_all_transactions(db_session)
        assert len(transactions) == 0
    
    def test_get_all_transactions_multiple(self, db_session):
        """Test getting all transactions when multiple exist"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        create_transaction(db_session, user.user_id, company.company_id, 100)
        create_transaction(db_session, user.user_id, company.company_id, 200)
        create_transaction(db_session, user.user_id, company.company_id, 300)
        
        transactions = get_all_transactions(db_session)
        assert len(transactions) == 3
    
    def test_get_transactions_by_user(self, db_session):
        """Test getting transactions for a specific user"""
        user1 = create_user(db_session, "User1", "Test", date(1990, 1, 1), "Addr1")
        user2 = create_user(db_session, "User2", "Test", date(1991, 1, 1), "Addr2")
        company = create_company(db_session, "Tech Corp", "Location")
        
        create_transaction(db_session, user1.user_id, company.company_id, 100)
        create_transaction(db_session, user1.user_id, company.company_id, 200)
        create_transaction(db_session, user2.user_id, company.company_id, 300)
        
        user1_transactions = get_transactions_by_user(db_session, user1.user_id)
        assert len(user1_transactions) == 2
        
        user2_transactions = get_transactions_by_user(db_session, user2.user_id)
        assert len(user2_transactions) == 1
    
    def test_get_transactions_by_company(self, db_session):
        """Test getting transactions for a specific company"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company1 = create_company(db_session, "Company1", "Loc1")
        company2 = create_company(db_session, "Company2", "Loc2")
        
        create_transaction(db_session, user.user_id, company1.company_id, 100)
        create_transaction(db_session, user.user_id, company1.company_id, 200)
        create_transaction(db_session, user.user_id, company2.company_id, 300)
        
        company1_transactions = get_transactions_by_company(db_session, company1.company_id)
        assert len(company1_transactions) == 2
        
        company2_transactions = get_transactions_by_company(db_session, company2.company_id)
        assert len(company2_transactions) == 1
    
    def test_get_transactions_by_user_and_company(self, db_session):
        """Test getting transactions for a specific user-company pair"""
        user1 = create_user(db_session, "User1", "Test", date(1990, 1, 1), "Addr1")
        user2 = create_user(db_session, "User2", "Test", date(1991, 1, 1), "Addr2")
        company1 = create_company(db_session, "Company1", "Loc1")
        company2 = create_company(db_session, "Company2", "Loc2")
        
        create_transaction(db_session, user1.user_id, company1.company_id, 100)
        create_transaction(db_session, user1.user_id, company1.company_id, 200)
        create_transaction(db_session, user1.user_id, company2.company_id, 300)
        create_transaction(db_session, user2.user_id, company1.company_id, 400)
        
        transactions = get_transactions_by_user_and_company(
            db_session, user1.user_id, company1.company_id
        )
        assert len(transactions) == 2
    
    def test_get_transactions_by_nonexistent_user(self, db_session):
        """Test getting transactions for a non-existent user"""
        transactions = get_transactions_by_user(db_session, "C999")
        assert len(transactions) == 0
    
    def test_get_transactions_by_nonexistent_company(self, db_session):
        """Test getting transactions for a non-existent company"""
        transactions = get_transactions_by_company(db_session, "C999")
        assert len(transactions) == 0


class TestTransactionUpdate:
    """Test cases for updating transactions"""
    
    def test_update_transaction_all_fields(self, db_session):
        """Test updating all fields of a transaction"""
        user1 = create_user(db_session, "User1", "Test", date(1990, 1, 1), "Addr1")
        user2 = create_user(db_session, "User2", "Test", date(1991, 1, 1), "Addr2")
        company1 = create_company(db_session, "Company1", "Loc1")
        company2 = create_company(db_session, "Company2", "Loc2")
        
        transaction = create_transaction(
            db_session, user1.user_id, company1.company_id, 100
        )
        
        new_datetime = datetime(2024, 2, 1, 12, 0, 0)
        updated = update_transaction(
            db=db_session,
            transaction_id=transaction.transaction_id,
            user_id=user2.user_id,
            company_id=company2.company_id,
            number_of_shares=500,
            transaction_datetime=new_datetime
        )
        
        assert updated.user_id == user2.user_id
        assert updated.company_id == company2.company_id
        assert updated.number_of_shares == 500
        assert updated.transaction_datetime == new_datetime
    
    def test_update_transaction_partial(self, db_session):
        """Test updating only some fields"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db_session, user.user_id, company.company_id, 100
        )
        
        updated = update_transaction(
            db=db_session,
            transaction_id=transaction.transaction_id,
            number_of_shares=200
        )
        
        assert updated.user_id == user.user_id  # Unchanged
        assert updated.company_id == company.company_id  # Unchanged
        assert updated.number_of_shares == 200  # Changed
    
    def test_update_transaction_nonexistent(self, db_session):
        """Test updating a non-existent transaction"""
        updated = update_transaction(
            db=db_session,
            transaction_id=999,
            number_of_shares=100
        )
        assert updated is None
    
    def test_update_transaction_to_zero_shares(self, db_session):
        """Test updating transaction shares to zero"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db_session, user.user_id, company.company_id, 100
        )
        
        updated = update_transaction(
            db=db_session,
            transaction_id=transaction.transaction_id,
            number_of_shares=0
        )
        
        assert updated.number_of_shares == 0


class TestTransactionDelete:
    """Test cases for deleting transactions"""
    
    def test_delete_transaction_existing(self, db_session):
        """Test deleting an existing transaction"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db_session, user.user_id, company.company_id, 100
        )
        
        result = delete_transaction(db_session, transaction.transaction_id)
        assert result is True
        
        deleted = get_transaction(db_session, transaction.transaction_id)
        assert deleted is None
    
    def test_delete_transaction_nonexistent(self, db_session):
        """Test deleting a non-existent transaction"""
        result = delete_transaction(db_session, "T999")
        assert result is False
    
    def test_delete_transaction_multiple(self, db_session):
        """Test deleting multiple transactions"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        trans1 = create_transaction(db_session, user.user_id, company.company_id, 100)
        trans2 = create_transaction(db_session, user.user_id, company.company_id, 200)
        trans3 = create_transaction(db_session, user.user_id, company.company_id, 300)
        
        delete_transaction(db_session, trans2.transaction_id)
        
        transactions = get_all_transactions(db_session)
        assert len(transactions) == 2
        assert trans1.transaction_id in [t.transaction_id for t in transactions]
        assert trans3.transaction_id in [t.transaction_id for t in transactions]

