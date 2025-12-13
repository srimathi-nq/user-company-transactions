from sqlalchemy import Column, String, Date, Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import re
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, firstname={self.firstname}, lastname={self.lastname})>"


class Company(Base):
    __tablename__ = "companies"
    
    company_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<Company(company_id={self.company_id}, name={self.name}, location={self.location})>"


class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.company_id"), nullable=False, index=True)
    number_of_shares = Column(Integer, nullable=False)
    transaction_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="transactions")
    company = relationship("Company", backref="transactions")
    
    def __repr__(self):
        return f"<Transaction(transaction_id={self.transaction_id}, user_id={self.user_id}, company_id={self.company_id}, shares={self.number_of_shares}, datetime={self.transaction_datetime})>"

