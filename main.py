from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List

# Define the Task model
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str

# Setup database
sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Create FastAPI app
app = FastAPI()

# Add CORS so HTML can fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Routes
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    with Session(engine) as session:
        return session.exec(select(Task)).all()

@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
