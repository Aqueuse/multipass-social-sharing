import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\jaima\\Desktop\\multipass.db')

database = declarative_base(bind=engine)
database.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()


class TwitterTask(database):
    __tablename__ = 'TwitterTask'
    task_id = Column(Integer(), primary_key=True, unique=True, nullable=False)
    message = Column(String(), unique=False, nullable=False)
    files = Column(String(), unique=False, nullable=False)

    def __init__(self, task_id, message, files):
        self.task_id = task_id
        self.message = message
        self.files = files


def create_database_if_not_exist():
    if not sqlalchemy.inspect(engine).has_table("TwitterTask"):
        print("twitter Task Table not exist")
        database.metadata.create_all()
        create_twitter_task(0, "empty", "empty")
        delete_twitter_task(0)


def create_twitter_task(task_id, message, files):
    new_twitter_task = TwitterTask(task_id=task_id, message=message, files=files)
    session.add(new_twitter_task)
    session.commit()


def get_twitter_task(task_id):
    for twitter_task in session.query(TwitterTask).filter(TwitterTask.task_id == task_id):
        return twitter_task


def twitter_task_exist(task_id):
    twitter_task = session.query(TwitterTask).filter(TwitterTask.task_id == task_id).all()
    if len(twitter_task) == 0:
        return False
    return True


def update_twitter_task(task_id, name, date, repetition, days, months):
    session.query(TwitterTask).filter(TwitterTask.task_id == task_id).update({
        TwitterTask.name: name,
        TwitterTask.date: date,
        TwitterTask.repetition: repetition,
        TwitterTask.days: days,
        TwitterTask.months: months}, synchronize_session=False)
    session.commit()


def delete_twitter_task(task_id):
    session.query(TwitterTask).filter(TwitterTask.task_id == task_id).delete()
    session.commit()
