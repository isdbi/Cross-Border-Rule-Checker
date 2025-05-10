from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class LegalRule(Base):
    __tablename__ = "legal_rules"
    id          = Column(Integer, primary_key=True, index=True)
    country     = Column(String, index=True)
    rule        = Column(String)
    replacement = Column(String)
    legal_source = Column(String, nullable=False)    # e.g. “AAOIFI 2024 §3.2”
    status       = Column(String, default="active")  # so you can filter only active ones
