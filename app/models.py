from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class BirthdayRecord(Base):
    __tablename__ = "birthdays"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)