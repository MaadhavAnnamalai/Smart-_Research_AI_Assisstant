from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./research_assistant.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    credits_remaining = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)

class ResearchReport(Base):
    __tablename__ = "research_reports"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    question = Column(Text)
    summary = Column(Text)
    key_takeaways = Column(Text)  # JSON string
    citations = Column(Text)  # JSON string
    sources_used = Column(Text)  # JSON string
    generated_at = Column(DateTime, default=datetime.utcnow)
    credits_used = Column(Integer, default=1)
    freshness_score = Column(Float, default=0.0)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    filename = Column(String)
    file_type = Column(String)
    size = Column(Integer)
    processed_at = Column(DateTime, default=datetime.utcnow)
    chunks = Column(Integer, default=0)
    file_path = Column(String)

class BillingEvent(Base):
    __tablename__ = "billing_events"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    event_type = Column(String)
    credits_used = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")
    description = Column(Text)
    config = Column(Text)  # JSON string

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
