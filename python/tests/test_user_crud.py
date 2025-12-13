import pytest
from datetime import date, datetime
from decimal import Decimal
from crud import (
    create_user, get_user, get_all_users, update_user, delete_user
)
from models import User


class TestUserCreate:
    """Test cases for creating users"""
    
    def test_create_user_basic(self, db_session):
        """Test creating a basic user with all required fields"""
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 5, 15),
            address="123 Main St",
            balance=Decimal('1000.00')
        )
        assert user.user_id == "U1"
        assert user.firstname == "John"
        assert user.lastname == "Doe"
        assert user.date_of_birth == date(1990, 5, 15)
        assert user.address == "123 Main St"
        assert user.balance == Decimal('1000.00')
    
    def test_create_user_minimal(self, db_session):
        """Test creating a user with minimal required fields"""
        user = create_user(
            db=db_session,
            firstname="Jane",
            lastname="Smith",
            date_of_birth=date(1985, 1, 1),
            address="456 Oak Ave"
        )
        assert user.user_id == "U1"
        assert user.balance == Decimal('0.00')  # Default balance
    
    def test_create_user_zero_balance(self, db_session):
        """Test creating a user with zero balance"""
        user = create_user(
            db=db_session,
            firstname="Bob",
            lastname="Wilson",
            date_of_birth=date(1995, 3, 20),
            address="789 Pine Rd",
            balance=Decimal('0.00')
        )
        assert user.balance == Decimal('0.00')
    
    def test_create_user_negative_balance(self, db_session):
        """Test creating a user with negative balance (edge case)"""
        user = create_user(
            db=db_session,
            firstname="Alice",
            lastname="Brown",
            date_of_birth=date(1992, 7, 10),
            address="321 Elm St",
            balance=Decimal('-50.00')
        )
        assert user.balance == Decimal('-50.00')
    
    def test_create_user_large_balance(self, db_session):
        """Test creating a user with very large balance"""
        user = create_user(
            db=db_session,
            firstname="Rich",
            lastname="Person",
            date_of_birth=date(1980, 1, 1),
            address="1 Billionaire Ave",
            balance=Decimal('9999999.99')
        )
        assert user.balance == Decimal('9999999.99')
    
    def test_create_user_decimal_precision(self, db_session):
        """Test creating a user with precise decimal balance"""
        user = create_user(
            db=db_session,
            firstname="Precise",
            lastname="User",
            date_of_birth=date(1991, 1, 1),
            address="123 Test St",
            balance=Decimal('1234.56')
        )
        assert user.balance == Decimal('1234.56')
    
    def test_create_multiple_users_auto_id(self, db_session):
        """Test that user IDs are auto-generated sequentially"""
        user1 = create_user(
            db=db_session,
            firstname="First",
            lastname="User",
            date_of_birth=date(1990, 1, 1),
            address="Address 1"
        )
        user2 = create_user(
            db=db_session,
            firstname="Second",
            lastname="User",
            date_of_birth=date(1991, 1, 1),
            address="Address 2"
        )
        user3 = create_user(
            db=db_session,
            firstname="Third",
            lastname="User",
            date_of_birth=date(1992, 1, 1),
            address="Address 3"
        )
        assert user1.user_id == "U1"
        assert user2.user_id == "U2"
        assert user3.user_id == "U3"
    
    def test_create_user_old_date(self, db_session):
        """Test creating a user with very old date of birth"""
        user = create_user(
            db=db_session,
            firstname="Old",
            lastname="Person",
            date_of_birth=date(1950, 1, 1),
            address="Old Address"
        )
        assert user.date_of_birth == date(1950, 1, 1)
    
    def test_create_user_future_date(self, db_session):
        """Test creating a user with future date (edge case - should still work)"""
        user = create_user(
            db=db_session,
            firstname="Future",
            lastname="Person",
            date_of_birth=date(2100, 1, 1),
            address="Future Address"
        )
        assert user.date_of_birth == date(2100, 1, 1)
    
    def test_create_user_long_address(self, db_session):
        """Test creating a user with very long address"""
        long_address = "A" * 500
        user = create_user(
            db=db_session,
            firstname="Long",
            lastname="Address",
            date_of_birth=date(1990, 1, 1),
            address=long_address
        )
        assert user.address == long_address
    
    def test_create_user_special_characters(self, db_session):
        """Test creating a user with special characters in name"""
        user = create_user(
            db=db_session,
            firstname="José",
            lastname="O'Connor-Smith",
            date_of_birth=date(1990, 1, 1),
            address="123 Main St, Apt #4-B"
        )
        assert user.firstname == "José"
        assert user.lastname == "O'Connor-Smith"


class TestUserRead:
    """Test cases for reading users"""
    
    def test_get_user_existing(self, db_session):
        """Test getting an existing user"""
        created = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 5, 15),
            address="123 Main St",
            balance=Decimal('1000.00')
        )
        user = get_user(db_session, created.user_id)
        assert user is not None
        assert user.user_id == created.user_id
        assert user.firstname == "John"
    
    def test_get_user_nonexistent(self, db_session):
        """Test getting a non-existent user"""
        user = get_user(db_session, "C999")
        assert user is None
    
    def test_get_user_empty_id(self, db_session):
        """Test getting a user with empty ID"""
        user = get_user(db_session, "")
        assert user is None
    
    def test_get_all_users_empty(self, db_session):
        """Test getting all users when none exist"""
        users = get_all_users(db_session)
        assert len(users) == 0
    
    def test_get_all_users_multiple(self, db_session):
        """Test getting all users when multiple exist"""
        create_user(db_session, "John", "Doe", date(1990, 1, 1), "Addr1")
        create_user(db_session, "Jane", "Smith", date(1991, 1, 1), "Addr2")
        create_user(db_session, "Bob", "Wilson", date(1992, 1, 1), "Addr3")
        
        users = get_all_users(db_session)
        assert len(users) == 3
    
    def test_get_all_users_with_limit(self, db_session):
        """Test getting all users with limit"""
        for i in range(5):
            create_user(db_session, f"User{i}", "Test", date(1990, 1, 1), f"Addr{i}")
        
        users = get_all_users(db_session, limit=3)
        assert len(users) == 3
    
    def test_get_all_users_with_skip(self, db_session):
        """Test getting all users with skip"""
        for i in range(5):
            create_user(db_session, f"User{i}", "Test", date(1990, 1, 1), f"Addr{i}")
        
        users = get_all_users(db_session, skip=2)
        assert len(users) == 3  # Should get users 3, 4, 5


class TestUserUpdate:
    """Test cases for updating users"""
    
    def test_update_user_all_fields(self, db_session):
        """Test updating all fields of a user"""
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 5, 15),
            address="123 Main St",
            balance=Decimal('1000.00')
        )
        
        updated = update_user(
            db=db_session,
            user_id=user.user_id,
            firstname="Jane",
            lastname="Smith",
            date_of_birth=date(1991, 6, 20),
            address="456 Oak Ave",
            balance=Decimal('2000.00')
        )
        
        assert updated.firstname == "Jane"
        assert updated.lastname == "Smith"
        assert updated.date_of_birth == date(1991, 6, 20)
        assert updated.address == "456 Oak Ave"
        assert updated.balance == Decimal('2000.00')
    
    def test_update_user_partial(self, db_session):
        """Test updating only some fields"""
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 5, 15),
            address="123 Main St",
            balance=Decimal('1000.00')
        )
        
        updated = update_user(
            db=db_session,
            user_id=user.user_id,
            balance=Decimal('5000.00')
        )
        
        assert updated.firstname == "John"  # Unchanged
        assert updated.balance == Decimal('5000.00')  # Changed
    
    def test_update_user_nonexistent(self, db_session):
        """Test updating a non-existent user"""
        updated = update_user(
            db=db_session,
            user_id="C999",
            firstname="New"
        )
        assert updated is None
    
    def test_update_user_balance_to_zero(self, db_session):
        """Test updating user balance to zero"""
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 1, 1),
            address="123 Main St",
            balance=Decimal('1000.00')
        )
        
        updated = update_user(db_session, user.user_id, balance=Decimal('0.00'))
        assert updated.balance == Decimal('0.00')
    
    def test_update_user_balance_to_negative(self, db_session):
        """Test updating user balance to negative"""
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 1, 1),
            address="123 Main St",
            balance=Decimal('1000.00')
        )
        
        updated = update_user(db_session, user.user_id, balance=Decimal('-100.00'))
        assert updated.balance == Decimal('-100.00')


class TestUserDelete:
    """Test cases for deleting users"""
    
    def test_delete_user_existing(self, db_session):
        """Test deleting an existing user"""
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 1, 1),
            address="123 Main St"
        )
        
        result = delete_user(db_session, user.user_id)
        assert result is True
        
        deleted = get_user(db_session, user.user_id)
        assert deleted is None
    
    def test_delete_user_nonexistent(self, db_session):
        """Test deleting a non-existent user"""
        result = delete_user(db_session, "C999")
        assert result is False
    
    def test_delete_user_with_transactions(self, db_session):
        """Test deleting a user that has transactions"""
        from crud import create_transaction, create_company
        
        user = create_user(
            db=db_session,
            firstname="John",
            lastname="Doe",
            date_of_birth=date(1990, 1, 1),
            address="123 Main St"
        )
        
        company = create_company(db_session, "Test Corp", "Location")
        
        # Create transactions
        create_transaction(db_session, user.user_id, company.company_id, 100)
        create_transaction(db_session, user.user_id, company.company_id, 50)
        
        # Delete user - should also delete transactions
        result = delete_user(db_session, user.user_id)
        assert result is True
        
        # Verify user is deleted
        assert get_user(db_session, user.user_id) is None
        
        # Verify transactions are deleted
        from crud import get_transactions_by_user
        transactions = get_transactions_by_user(db_session, user.user_id)
        assert len(transactions) == 0

