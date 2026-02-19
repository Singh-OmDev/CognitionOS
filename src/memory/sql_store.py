from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from src.core.config import settings

Base = declarative_base()

class TaskLog(Base):
    __tablename__ = "task_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, index=True) # UUID for the task
    task_name = Column(String)
    status = Column(String) # 'running', 'completed', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    steps = relationship("TaskStep", back_populates="task")

class TaskStep(Base):
    __tablename__ = "task_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    task_log_id = Column(Integer, ForeignKey("task_logs.id"))
    step_number = Column(Integer)
    agent_name = Column(String)
    action = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    task = relationship("TaskLog", back_populates="steps")

class InteractionHistory(Base):
    __tablename__ = "interaction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String) # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SQLStore:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    def log_task(self, task_id: str, name: str, status: str):
        with self.SessionLocal() as session:
            log = TaskLog(task_id=task_id, task_name=name, status=status)
            session.add(log)
            session.commit()
            return log.id

    def update_task_status(self, task_id: str, status: str):
         with self.SessionLocal() as session:
            log = session.query(TaskLog).filter(TaskLog.task_id == task_id).first()
            if log:
                log.status = status
                session.commit()

    def log_step(self, task_id: str, step_num: int, agent: str, action: str, input_d: dict, output_d: dict):
        with self.SessionLocal() as session:
            # Find parent task
            task = session.query(TaskLog).filter(TaskLog.task_id == task_id).first()
            if task:
                step = TaskStep(
                    task_log_id=task.id,
                    step_number=step_num,
                    agent_name=agent,
                    action=action,
                    input_data=input_d,
                    output_data=output_d
                )
                session.add(step)
                session.commit()

    def log_interaction(self, session_id: str, role: str, content: str):
        with self.SessionLocal() as session:
            interaction = InteractionHistory(session_id=session_id, role=role, content=content)
            session.add(interaction)
            session.commit()
