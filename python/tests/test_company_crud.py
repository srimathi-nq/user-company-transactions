import pytest
from datetime import date
from crud import (
    create_company, get_company, get_all_companies, update_company, delete_company
)
from models import Company


class TestCompanyCreate:
    """Test cases for creating companies"""
    
    def test_create_company_basic(self, db_session):
        """Test creating a basic company"""
        company = create_company(
            db=db_session,
            name="Tech Solutions Inc",
            location="San Francisco, CA"
        )
        assert company.company_id == "C1"
        assert company.name == "Tech Solutions Inc"
        assert company.location == "San Francisco, CA"
    
    def test_create_company_minimal(self, db_session):
        """Test creating a company with minimal fields"""
        company = create_company(
            db=db_session,
            name="ABC",
            location="XYZ"
        )
        assert company.name == "ABC"
        assert company.location == "XYZ"
    
    def test_create_multiple_companies_auto_id(self, db_session):
        """Test that company IDs are auto-generated sequentially"""
        company1 = create_company(db_session, "Company 1", "Location 1")
        company2 = create_company(db_session, "Company 2", "Location 2")
        company3 = create_company(db_session, "Company 3", "Location 3")
        
        assert company1.company_id == "C1"
        assert company2.company_id == "C2"
        assert company3.company_id == "C3"
    
    def test_create_company_long_name(self, db_session):
        """Test creating a company with very long name"""
        long_name = "A" * 500
        company = create_company(db_session, long_name, "Location")
        assert company.name == long_name
    
    def test_create_company_long_location(self, db_session):
        """Test creating a company with very long location"""
        long_location = "B" * 500
        company = create_company(db_session, "Company", long_location)
        assert company.location == long_location
    
    def test_create_company_special_characters(self, db_session):
        """Test creating a company with special characters"""
        company = create_company(
            db=db_session,
            name="O'Brien & Sons, LLC",
            location="São Paulo, Brazil"
        )
        assert company.name == "O'Brien & Sons, LLC"
        assert company.location == "São Paulo, Brazil"
    
    def test_create_company_empty_strings(self, db_session):
        """Test creating a company with empty strings (edge case)"""
        company = create_company(db_session, "", "")
        assert company.name == ""
        assert company.location == ""
    
    def test_create_company_numbers_in_name(self, db_session):
        """Test creating a company with numbers in name"""
        company = create_company(db_session, "Company 123", "Location 456")
        assert company.name == "Company 123"
        assert company.location == "Location 456"


class TestCompanyRead:
    """Test cases for reading companies"""
    
    def test_get_company_existing(self, db_session):
        """Test getting an existing company"""
        created = create_company(db_session, "Test Corp", "Test Location")
        company = get_company(db_session, created.company_id)
        
        assert company is not None
        assert company.company_id == created.company_id
        assert company.name == "Test Corp"
    
    def test_get_company_nonexistent(self, db_session):
        """Test getting a non-existent company"""
        company = get_company(db_session, "C999")
        assert company is None
    
    def test_get_company_empty_id(self, db_session):
        """Test getting a company with empty ID"""
        company = get_company(db_session, "")
        assert company is None
    
    def test_get_all_companies_empty(self, db_session):
        """Test getting all companies when none exist"""
        companies = get_all_companies(db_session)
        assert len(companies) == 0
    
    def test_get_all_companies_multiple(self, db_session):
        """Test getting all companies when multiple exist"""
        create_company(db_session, "Company 1", "Location 1")
        create_company(db_session, "Company 2", "Location 2")
        create_company(db_session, "Company 3", "Location 3")
        
        companies = get_all_companies(db_session)
        assert len(companies) == 3
    
    def test_get_all_companies_with_limit(self, db_session):
        """Test getting all companies with limit"""
        for i in range(5):
            create_company(db_session, f"Company {i}", f"Location {i}")
        
        companies = get_all_companies(db_session, limit=3)
        assert len(companies) == 3
    
    def test_get_all_companies_with_skip(self, db_session):
        """Test getting all companies with skip"""
        for i in range(5):
            create_company(db_session, f"Company {i}", f"Location {i}")
        
        companies = get_all_companies(db_session, skip=2)
        assert len(companies) == 3


class TestCompanyUpdate:
    """Test cases for updating companies"""
    
    def test_update_company_all_fields(self, db_session):
        """Test updating all fields of a company"""
        company = create_company(db_session, "Old Name", "Old Location")
        
        updated = update_company(
            db=db_session,
            company_id=company.company_id,
            name="New Name",
            location="New Location"
        )
        
        assert updated.name == "New Name"
        assert updated.location == "New Location"
    
    def test_update_company_name_only(self, db_session):
        """Test updating only company name"""
        company = create_company(db_session, "Old Name", "Location")
        
        updated = update_company(
            db=db_session,
            company_id=company.company_id,
            name="New Name"
        )
        
        assert updated.name == "New Name"
        assert updated.location == "Location"  # Unchanged
    
    def test_update_company_location_only(self, db_session):
        """Test updating only company location"""
        company = create_company(db_session, "Name", "Old Location")
        
        updated = update_company(
            db=db_session,
            company_id=company.company_id,
            location="New Location"
        )
        
        assert updated.name == "Name"  # Unchanged
        assert updated.location == "New Location"
    
    def test_update_company_nonexistent(self, db_session):
        """Test updating a non-existent company"""
        updated = update_company(
            db=db_session,
            company_id="C999",
            name="New Name"
        )
        assert updated is None
    
    def test_update_company_to_empty_strings(self, db_session):
        """Test updating company to empty strings"""
        company = create_company(db_session, "Name", "Location")
        
        updated = update_company(
            db=db_session,
            company_id=company.company_id,
            name="",
            location=""
        )
        
        assert updated.name == ""
        assert updated.location == ""


class TestCompanyDelete:
    """Test cases for deleting companies"""
    
    def test_delete_company_existing(self, db_session):
        """Test deleting an existing company"""
        company = create_company(db_session, "Test Corp", "Location")
        
        result = delete_company(db_session, company.company_id)
        assert result is True
        
        deleted = get_company(db_session, company.company_id)
        assert deleted is None
    
    def test_delete_company_nonexistent(self, db_session):
        """Test deleting a non-existent company"""
        result = delete_company(db_session, "C999")
        assert result is False
    
    def test_delete_company_with_transactions(self, db_session):
        """Test deleting a company that has transactions"""
        from crud import create_user, create_transaction
        
        user = create_user(
            db_session,
            "John", "Doe", 
            date(1990, 1, 1), 
            "Address"
        )
        company = create_company(db_session, "Test Corp", "Location")
        
        # Create transactions
        create_transaction(db_session, user.user_id, company.company_id, 100)
        create_transaction(db_session, user.user_id, company.company_id, 50)
        
        # Delete company - should also delete transactions
        result = delete_company(db_session, company.company_id)
        assert result is True
        
        # Verify company is deleted
        assert get_company(db_session, company.company_id) is None
        
        # Verify transactions are deleted
        from crud import get_transactions_by_company
        transactions = get_transactions_by_company(db_session, company.company_id)
        assert len(transactions) == 0

