from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Couple(Base):
    __tablename__ = "couples"
    id = Column(String, primary_key=True, index=True) # Unique Couple ID (uuid)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("User", back_populates="couple")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    couple_id = Column(String, ForeignKey("couples.id"), nullable=True)
    
    couple = relationship("Couple", back_populates="users")
    memories = relationship("Memory", back_populates="user")
    conflicts = relationship("Conflict", back_populates="user")
    weekly_checks = relationship("WeeklyCheck", back_populates="user")

class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    emotion = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="memories")

class Conflict(Base):
    __tablename__ = "conflicts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    severity = Column(Integer)
    reason = Column(String)
    resolved = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="conflicts")

class WeeklyCheck(Base):
    __tablename__ = "weekly_checks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(String)
    conflict_status = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="weekly_checks")
