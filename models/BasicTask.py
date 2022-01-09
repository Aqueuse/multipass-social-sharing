import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine, func

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\jaima\\Desktop\\multipass.db')

database = declarative_base(bind=engine)
database.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()


class BasicTask(database):
    __tablename__ = 'basicTask'
    task_id = Column(Integer(), primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer(), unique=False, nullable=False)
    name = Column(String(), unique=False, nullable=False)
    date = Column(String(), unique=False, nullable=False)
    repetition = Column(String(), unique=False, nullable=False)
    days = Column(String(), unique=False, nullable=False)
    months = Column(String(), unique=False, nullable=False)

    def __init__(self, task_id, user_id, name, date, repetition, days, months):
        self.task_id = task_id
        self.user_id = user_id
        self.name = name
        self.date = date
        self.repetition = repetition
        self.days = days
        self.months = months


def create_database_if_not_exist():
    if not sqlalchemy.inspect(engine).has_table("basicTask"):
        print("basic Task Table not exist")
        database.metadata.create_all()
        create_basic_task(0, 0, "empty", "empty", "empty", "empty", "empty")
        delete_basic_task(0)


def create_basic_task(task_id, user_id, name, date, repetition, days, months):
    new_basic_task = BasicTask(
        task_id=task_id,
        user_id=user_id,
        name=name, date=date,
        repetition=repetition,
        days=days,
        months=months
    )
    session.add(new_basic_task)
    session.commit()


def get_basic_task(task_id):
    for basic_task in session.query(BasicTask).filter(BasicTask.task_id == task_id):
        return basic_task


def get_user_basic_tasks(user_id):
    return session.query(BasicTask).filter(BasicTask.user_id == user_id).all()


def get_max_task_id():
    return session.query(func.max(BasicTask.task_id)).scalar()


def basic_task_exist(task_id):
    basic_task = session.query(BasicTask).filter(BasicTask.task_id == task_id).all()
    if len(basic_task) == 0:
        return False
    return True


def update_basic_task(task_id, name, date, repetition, days, months):
    session.query(BasicTask).filter(BasicTask.task_id == task_id).update({
        BasicTask.name: name,
        BasicTask.date: date,
        BasicTask.repetition: repetition,
        BasicTask.days: days,
        BasicTask.months: months}, synchronize_session=False)
    session.commit()


def delete_basic_task(task_id):
    session.query(BasicTask).filter(BasicTask.task_id == task_id).delete()
    session.commit()
