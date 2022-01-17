import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////srv/multipass.db')

database = declarative_base(bind=engine)
database.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()


class InstagrmTask(database):
    __tablename__ = 'InstagrmTask'
    task_id = Column(Integer(), primary_key=True, unique=True, nullable=False)
    message = Column(String(), unique=False, nullable=False)
    files = Column(String(), unique=False, nullable=False)

    def __init__(self, task_id, message, files):
        self.task_id = task_id
        self.message = message
        self.files = files


def create_database_if_not_exist():
    if not sqlalchemy.inspect(engine).has_table("InstagrmTask"):
        print("instagram Task Table not exist")
        database.metadata.create_all()
        create_instagram_task(0, "empty", "empty")
        delete_instagram_task(0)


def create_instagram_task(task_id, message, files):
    new_instagram_task = InstagrmTask(task_id=task_id, message=message, files=files)
    session.add(new_instagram_task)
    session.commit()


def get_instagram_task(task_id):
    for instagram_task in session.query(InstagrmTask).filter(InstagrmTask.task_id == task_id):
        return instagram_task


def instagram_task_exist(task_id):
    instagram_task = session.query(InstagrmTask).filter(InstagrmTask.task_id == task_id).all()
    if len(instagram_task) == 0:
        return False
    return True


def update_instagram_task(task_id, name, date, repetition, days, months):
    session.query(InstagrmTask).filter(InstagrmTask.task_id == task_id).update({
        InstagrmTask.name: name,
        InstagrmTask.date: date,
        InstagrmTask.repetition: repetition,
        InstagrmTask.days: days,
        InstagrmTask.months: months}, synchronize_session=False)
    session.commit()


def delete_instagram_task(task_id):
    session.query(InstagrmTask).filter(InstagrmTask.task_id == task_id).delete()
    session.commit()
