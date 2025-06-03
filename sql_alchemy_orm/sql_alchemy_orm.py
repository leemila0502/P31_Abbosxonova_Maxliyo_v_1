# from unittest.mock import Base
import tabulate
from sqlalchemy import create_engine, Text, text, Column, Integer, String

# from sqlalchemy.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = 'database.db'

#
engine = create_engine('sqlite:///'+db_url)
base= declarative_base()
# conn = engine.connect()
# query = "CREATE TABLE people(id   integer primary key aubot_dbtoincrement, name text    not null, age  integer not null";
# conn.execute(text(query))

class People(base):
    __tablename__='people'
    id=Column(Integer, primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=False)
    age=Column(Integer,nullable=False)


    def __repr__(self):
        return f"{self.__class__.__name__} (name={self.name}, age={self.age})"

    @property
    def is_adult(self):
        return self.age >= 18


    @property
    def greating(self):
        return f"Hello ({self.name})"

    @classmethod
    def display(cls,session):
        people=session.query(cls).all()
        people=[(p,p.is_adult,p.greating)for p in people]
        header=['OBYEKT','IS_ADULT','GREATING']
        print(tabulate.tabulate(people,header,tablefmt='simple_grid'))
        return people

    def save(self,session):
        session.add(self)
        session.commit()

    @classmethod
    def delate(cls,session,id_):
        obj=session.query(cls).filter(id_==cls.id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    @classmethod
    def get_by_id(cls,session,id_):
        return session.query(cls).filter(cls.id==id_).first()

    @classmethod
    def update(cls,session,id,**kwargs):
        obj = cls.get_by_id(session,id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    raise AttributeError(f"Attribute {key} not found.")
            session.commit()
            return True
        return False


base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
# p1=People(name='John',age=10)
# session.add(p1)
# session.commit()
# People.display(session)
# p1=People(name='Collin',age=25)
# p1.save(session)
# print(People.delate(session,4))
# print(session.query(People).all())
print(People.update(session,2,name='Aziza',age='20'))