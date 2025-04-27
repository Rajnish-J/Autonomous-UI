import argparse
import datetime
from database import SessionLocal
import repository
import models
from tabulate import tabulate

def list_sessions(args):
    """List all sessions or filter by active status."""
    with SessionLocal() as db:
        if args.active:
            sessions = repository.get_active_sessions(db)
        else:
            sessions = db.query(models.Session).all()
        
        if not sessions:
            print("No sessions found.")
            return
        
        session_data = []
        for session in sessions:
            session_data.append([
                session.id,
                session.created_at,
                session.closed_at or "Still active",
                session.is_active,
                len(session.tasks)
            ])
        
        headers = ["Session ID", "Created At", "Closed At", "Active", "Tasks Count"]
        print(tabulate(session_data, headers=headers, tablefmt="grid"))

def list_tasks(args):
    """List tasks for a specific session or all tasks."""
    with SessionLocal() as db:
        if args.session_id:
            tasks = repository.get_tasks_by_session_id(db, args.session_id)
        else:
            tasks = db.query(models.Task).all()
        
        if not tasks:
            print("No tasks found.")
            return
        
        task_data = []
        for task in tasks:
            task_data.append([
                task.id,
                task.session_id,
                task.task_description[:50] + "..." if len(task.task_description) > 50 else task.task_description,
                task.status,
                task.started_at,
                task.completed_at or ""
            ])
        
        headers = ["Task ID", "Session ID", "Description", "Status", "Started At", "Completed At"]
        print(tabulate(task_data, headers=headers, tablefmt="grid"))

def cleanup_sessions(args):
    """Mark all active sessions as closed."""
    with SessionLocal() as db:
        active_sessions = repository.get_active_sessions(db)
        count = 0
        for session in active_sessions:
            repository.close_session(db, session.id)
            count += 1
        print(f"Marked {count} sessions as closed.")

def main():
    parser = argparse.ArgumentParser(description="Database CLI for Anchor Browser Automation")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Sessions command
    sessions_parser = subparsers.add_parser("sessions", help="List sessions")
    sessions_parser.add_argument("--active", action="store_true", help="List only active sessions")
    sessions_parser.set_defaults(func=list_sessions)
    
    # Tasks command
    tasks_parser = subparsers.add_parser("tasks", help="List tasks")
    tasks_parser.add_argument("--session-id", help="Filter tasks by session ID")
    tasks_parser.set_defaults(func=list_tasks)
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Cleanup stale sessions")
    cleanup_parser.set_defaults(func=cleanup_sessions)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()