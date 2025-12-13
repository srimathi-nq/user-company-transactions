import pytest
from datetime import date, datetime
from decimal import Decimal
from crud import (
    create_user, get_user, update_user, delete_user,
    create_company, get_company, update_company, delete_company,
    create_transaction, get_transaction, update_transaction, delete_transaction,
    get_all_users, get_all_companies, get_all_transactions,
    get_transactions_by_user, get_transactions_by_company
)


class TestCRUDOrder:
    """Test various orders of CRUD operations"""
    
    def test_create_read_update_delete_sequence(self, db_session):
        """Test standard CRUD sequence: Create -> Read -> Update -> Delete"""
        # Create
        user = create_user(
            db_session, "John", "Doe", date(1990, 1, 1), "Address", Decimal('1000.00')
        )
        assert user.user_id == "U1"
        
        # Read
        read_user = get_user(db_session, "C1")
        assert read_user.firstname == "John"
        
        # Update
        updated = update_user(db_session, "C1", balance=Decimal('2000.00'))
        assert updated.balance == Decimal('2000.00')
        
        # Delete
        result = delete_user(db_session, "C1")
        assert result is True
        assert get_user(db_session, "C1") is None
    
    def test_create_update_before_read(self, db_session):
        """Test Create -> Update -> Read sequence"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        update_user(db_session, user.user_id, firstname="Jane")
        
        read_user = get_user(db_session, user.user_id)
        assert read_user.firstname == "Jane"
    
    def test_multiple_updates(self, db_session):
        """Test multiple updates on same record"""
        user = create_user(
            db_session, "John", "Doe", date(1990, 1, 1), "Address", Decimal('1000.00')
        )
        
        update_user(db_session, user.user_id, balance=Decimal('2000.00'))
        update_user(db_session, user.user_id, balance=Decimal('3000.00'))
        update_user(db_session, user.user_id, balance=Decimal('4000.00'))
        
        final_user = get_user(db_session, user.user_id)
        assert final_user.balance == Decimal('4000.00')
    
    def test_create_delete_create_same_id(self, db_session):
        """Test creating, deleting, then creating again (reuses ID if no other users exist)"""
        user1 = create_user(db_session, "User1", "Test", date(1990, 1, 1), "Addr1")
        user_id1 = user1.user_id
        
        delete_user(db_session, user_id1)
        
        # Create another user - should get C1 again since no users exist
        user2 = create_user(db_session, "User2", "Test", date(1991, 1, 1), "Addr2")
        user_id2 = user2.user_id
        
        # ID generation finds max from existing IDs, so if none exist, starts from U1
        assert user_id2 == "U1"
        
        # But if we create another user while U1 exists, it should get U2
        user3 = create_user(db_session, "User3", "Test", date(1992, 1, 1), "Addr3")
        assert user3.user_id == "U2"
    
    def test_user_company_transaction_chain(self, db_session):
        """Test creating user, company, then transaction"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(
            db_session, user.user_id, company.company_id, 100
        )
        
        assert transaction.user_id == user.user_id
        assert transaction.company_id == company.company_id
    
    def test_delete_user_with_transactions_cascade(self, db_session):
        """Test deleting user should delete related transactions"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        trans1 = create_transaction(db_session, user.user_id, company.company_id, 100)
        trans2 = create_transaction(db_session, user.user_id, company.company_id, 200)
        
        delete_user(db_session, user.user_id)
        
        assert get_user(db_session, user.user_id) is None
        assert get_transaction(db_session, trans1.transaction_id) is None
        assert get_transaction(db_session, trans2.transaction_id) is None
    
    def test_delete_company_with_transactions_cascade(self, db_session):
        """Test deleting company should delete related transactions"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        trans1 = create_transaction(db_session, user.user_id, company.company_id, 100)
        trans2 = create_transaction(db_session, user.user_id, company.company_id, 200)
        
        delete_company(db_session, company.company_id)
        
        assert get_company(db_session, company.company_id) is None
        assert get_transaction(db_session, trans1.transaction_id) is None
        assert get_transaction(db_session, trans2.transaction_id) is None
    
    def test_update_transaction_after_user_delete(self, db_session):
        """Test that transactions are deleted when user is deleted, so update fails"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(db_session, user.user_id, company.company_id, 100)
        trans_id = transaction.transaction_id
        
        delete_user(db_session, user.user_id)
        
        # Transaction should be deleted, so update should fail
        updated = update_transaction(db_session, trans_id, number_of_shares=200)
        assert updated is None
    
    def test_complex_workflow(self, db_session):
        """Test a complex workflow with multiple operations"""
        # Create users
        user1 = create_user(db_session, "User1", "Test", date(1990, 1, 1), "Addr1")
        user2 = create_user(db_session, "User2", "Test", date(1991, 1, 1), "Addr2")
        
        # Create companies
        company1 = create_company(db_session, "Company1", "Loc1")
        company2 = create_company(db_session, "Company2", "Loc2")
        
        # Create transactions
        trans1 = create_transaction(db_session, user1.user_id, company1.company_id, 100)
        trans2 = create_transaction(db_session, user1.user_id, company2.company_id, 200)
        trans3 = create_transaction(db_session, user2.user_id, company1.company_id, 300)
        
        # Update user
        update_user(db_session, user1.user_id, balance=Decimal('5000.00'))
        
        # Update company
        update_company(db_session, company1.company_id, location="New Location")
        
        # Update transaction
        update_transaction(db_session, trans1.transaction_id, number_of_shares=150)
        
        # Verify updates
        assert get_user(db_session, user1.user_id).balance == Decimal('5000.00')
        assert get_company(db_session, company1.company_id).location == "New Location"
        assert get_transaction(db_session, trans1.transaction_id).number_of_shares == 150
        
        # Delete one transaction
        delete_transaction(db_session, trans2.transaction_id)
        assert get_transaction(db_session, trans2.transaction_id) is None
        
        # Delete user (should cascade delete transactions)
        delete_user(db_session, user1.user_id)
        assert get_user(db_session, user1.user_id) is None
        assert get_transaction(db_session, trans1.transaction_id) is None
        
        # Remaining transaction should still exist
        assert get_transaction(db_session, trans3.transaction_id) is not None
    
    def test_read_all_after_multiple_operations(self, db_session):
        """Test reading all records after multiple create/delete operations"""
        # Create multiple records
        for i in range(5):
            create_user(db_session, f"User{i}", "Test", date(1990, 1, 1), f"Addr{i}")
        
        # Delete some
        delete_user(db_session, "C2")
        delete_user(db_session, "C4")
        
        # Read all
        users = get_all_users(db_session)
        assert len(users) == 3
        user_ids = [u.user_id for u in users]
        assert "C1" in user_ids
        assert "C3" in user_ids
        assert "C5" in user_ids
        assert "C2" not in user_ids
        assert "C4" not in user_ids
    
    def test_transaction_foreign_key_integrity(self, db_session):
        """Test that transactions maintain foreign key integrity"""
        user = create_user(db_session, "John", "Doe", date(1990, 1, 1), "Address")
        company = create_company(db_session, "Tech Corp", "Location")
        
        transaction = create_transaction(db_session, user.user_id, company.company_id, 100)
        
        # Verify relationships
        assert transaction.user_id == user.user_id
        assert transaction.company_id == company.company_id
        
        # Update user ID in transaction
        user2 = create_user(db_session, "Jane", "Smith", date(1991, 1, 1), "Addr2")
        update_transaction(db_session, transaction.transaction_id, user_id=user2.user_id)
        
        updated_trans = get_transaction(db_session, transaction.transaction_id)
        assert updated_trans.user_id == user2.user_id
    
    def test_bulk_operations(self, db_session):
        """Test performing bulk operations"""
        # Create many users
        for i in range(10):
            create_user(db_session, f"User{i}", "Test", date(1990, 1, 1), f"Addr{i}")
        
        # Create many companies
        for i in range(5):
            create_company(db_session, f"Company{i}", f"Loc{i}")
        
        # Create many transactions
        for i in range(10):
            user_id = f"C{i+1}"
            company_id = f"C{(i % 5) + 1}"
            create_transaction(db_session, user_id, company_id, (i+1) * 10)
        
        # Verify counts
        assert len(get_all_users(db_session)) == 10
        assert len(get_all_companies(db_session)) == 5
        assert len(get_all_transactions(db_session)) == 10
        
        # Delete all transactions for one user
        user_transactions = get_transactions_by_user(db_session, "C1")
        for trans in user_transactions:
            delete_transaction(db_session, trans.transaction_id)
        
        # Verify remaining transactions
        remaining = get_all_transactions(db_session)
        assert len(remaining) < 10

