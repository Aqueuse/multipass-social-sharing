import sqlalchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////srv/multipass.db')

database = declarative_base(bind=engine)
database.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()


def create_database_if_not_exist():
    if not sqlalchemy.inspect(engine).has_table("users"):
        print("user Table not exist")
        database.metadata.create_all()
        create_user("empty", "empty")
        delete_user("empty")


class User(database):
    __tablename__ = 'users'
    email = Column(String(30), primary_key=True, unique=True, nullable=False)
    password = Column(String(100), unique=False, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


def create_user(email, password):
    new_user = User(email=email, password=password)
    print("coin")
    session.add(new_user)
    session.commit()


def get_user(email):
    for user in session.query(User).filter(User.email == email):
        return user


def user_exist(email):
    user = session.query(User).filter(User.email == email).all()
    if len(user) == 0:
        return False
    return True


def update_user(email, new_password):
    session.query(User).filter(User.email == email).update({User.password: new_password}, synchronize_session=False)
    session.commit()


def delete_user(email):
    session.query(User).filter(User.email == email).delete()
    session.commit()
