from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
# engine = create_engine("postgresql://postgres:1111@localhost/mydb", echo=True)

# Session = sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    login = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    passport = Column(String)
    address = Column(String)
    email = Column(String)
    phone_number = Column(String)
    status = Column(String)

    def __init__(self, login, password, name, passport, address, email, phone_number, status):
        self.login = login
        self.password = password
        self.name = name
        self.passport = passport
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.status = status

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, login, password):
        from app import session
        user = session.query(cls).filter(cls.login == login).one()
        if not check_password_hash(user.password, password):
            raise Exception('No user with this password')
        return user


class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True, unique=True)
    all_money = Column(Integer)
    per_cent = Column(Integer)

    def __init__(self, all_money, per_cent):
        self.all_money = all_money
        self.per_cent = per_cent


class Credits(Base):
    __tablename__ = 'credits'
    id = Column(Integer, primary_key=True, unique=True)
    start_date = Column(String)
    end_date = Column(String)
    start_sum = Column(Integer)
    current_sum = Column(Integer)
    bank_id = Column(Integer, ForeignKey(Banks.id))
    user_id = Column(Integer, ForeignKey(Users.id))

    def __init__(self, start_date, end_date, start_sum, current_sum, bank_id, user_id):
        self.start_date = start_date
        self.end_date = end_date
        self.start_sum = start_sum
        self.current_sum = current_sum
        self.bank_id = bank_id
        self.user_id = user_id


class UserCredit(Base):
    __tablename__ = 'usercredit'
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    credit_id = Column(Integer, ForeignKey(Credits.id))

    def __init__(self, user_id, credit_id):
        self.user_id = user_id
        self.credit_id = credit_id

class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, unique=True)
    date = Column(String)
    summ = Column(Integer)
    credit_id = Column(Integer, ForeignKey(Credits.id))

    def __init__(self, date, summ, credit_id):
        self.date = date
        self.summ = summ
        self.credit_id = credit_id