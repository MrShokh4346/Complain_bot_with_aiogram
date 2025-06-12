from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from db.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_blocked = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    questions = relationship("Question", back_populates="user", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    is_answered = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime, nullable=True)

    # Relationship
    user = relationship("User", back_populates="questions")


