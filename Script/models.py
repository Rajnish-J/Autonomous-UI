from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(255), primary_key=True)
    cdp_url = Column(String(255), nullable=False)
    live_view_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    closed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="session")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey("sessions.id"))
    task_description = Column(Text, nullable=False)
    result = Column(JSON, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    
    # Relationship with session
    session = relationship("Session", back_populates="tasks")