import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////srv/multipass.db')

database = declarative_base(bind=engine)
database.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()


class FacebookTask(database):
    __tablename__ = 'FacebookTask'
    task_id = Column(Integer(), primary_key=True, unique=True, nullable=False)
    message = Column(String(), unique=False, nullable=False)
    files = Column(String(), unique=False, nullable=False)

    def __init__(self, task_id, message, files):
        self.task_id = task_id
        self.message = message
        self.files = files


def create_database_if_not_exist():
    if not sqlalchemy.inspect(engine).has_table("FacebookTask"):
        print("facebook Task Table not exist")
        database.metadata.create_all()
        create_facebook_task(0, "empty", "empty")
        delete_facebook_task(0)


def create_facebook_task(task_id, message, files):
    new_facebook_task = FacebookTask(task_id=task_id, message=message, files=files)
    session.add(new_facebook_task)
    session.commit()


def get_facebook_task(task_id):
    for facebook_task in session.query(FacebookTask).filter(FacebookTask.task_id == task_id):
        return facebook_task


def facebook_task_exist(task_id):
    facebook_task = session.query(FacebookTask).filter(FacebookTask.task_id == task_id).all()
    if len(facebook_task) == 0:
        return False
    return True


def update_facebook_task(task_id, name, date, repetition, days, months):
    session.query(FacebookTask).filter(FacebookTask.task_id == task_id).update({
        FacebookTask.name: name,
        FacebookTask.date: date,
        FacebookTask.repetition: repetition,
        FacebookTask.days: days,
        FacebookTask.months: months}, synchronize_session=False)
    session.commit()


def delete_facebook_task(task_id):
    session.query(FacebookTask).filter(FacebookTask.task_id == task_id).delete()
    session.commit()
