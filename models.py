from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:1111@localhost/mydb", echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, unique=True)
    name = Column('name', String, )
    passport = Column('passport', String)
    address = Column('address', String)
    email = Column('email', String)
    phone_number = Column('phone_number', String)
    money_amount = Column('money_amount', Integer)



class Banks(Base):
    __tablename__ = 'banks'
    id = Column('id', Integer, primary_key=True, unique=True)
    all_money = Column('all_money', Integer)
    per_cent = Column('per_cent', Integer)


class Credits(Base):
    __tablename__ = 'credits'
    id = Column('id', Integer, primary_key=True, unique=True)
    start_date = Column('start_date',String)
    end_date = Column('end_date', String)
    start_sum = Column('start_sum', Integer)
    current_sum = Column('current_sum', Integer, unique=True)
    bank_id = Column('bank_id', Integer, ForeignKey(Banks.id))


class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column('id', Integer, primary_key=True, unique=True)
    date = Column('date',String)
    summ = Column('summ', Integer, unique=False)
    credit_id = Column('credit_id', Integer, ForeignKey(Credits.id))

