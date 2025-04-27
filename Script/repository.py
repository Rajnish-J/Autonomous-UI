from sqlalchemy.orm import Session
import models
import datetime
import json

def create_session(db: Session, session_id: str, cdp_url: str, live_view_url: str) -> models.Session:
    """Create a new session in the database."""
    db_session = models.Session(
        id=session_id,
        cdp_url=cdp_url,
        live_view_url=live_view_url,
        is_active=True
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def close_session(db: Session, session_id: str) -> models.Session:
    """Mark a session as closed in the database."""
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if db_session:
        db_session.closed_at = datetime.datetime.now()
        db_session.is_active = False
        db.commit()
        db.refresh(db_session)
    return db_session

def create_task(db: Session, session_id: str, task_description: str) -> models.Task:
    """Create a new task in the database."""
    db_task = models.Task(
        session_id=session_id,
        task_description=task_description,
        status="running"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_result(db: Session, task_id: int, result, status: str = "completed") -> models.Task:
    """Update task result in the database."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.result = result if isinstance(result, dict) else {"result": str(result)}
        db_task.status = status
        db_task.completed_at = datetime.datetime.now()
        db.commit()
        db.refresh(db_task)
    return db_task

def get_active_sessions(db: Session, skip: int = 0, limit: int = 100):
    """Get all active sessions from the database."""
    return db.query(models.Session).filter(models.Session.is_active == True).offset(skip).limit(limit).all()

def get_tasks_by_session_id(db: Session, session_id: str, skip: int = 0, limit: int = 100):
    """Get all tasks for a specific session from the database."""
    return db.query(models.Task).filter(models.Task.session_id == session_id).offset(skip).limit(limit).all()