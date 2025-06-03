from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, ForeignKey)

from sql_alc.config import db_user, password, host, port, db_name
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

pg_url = f"postgresql+psycopg2://{db_user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(pg_url)

Base = declarative_base()


class User(Base):
    __tablename__ = 'userss'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False, unique=True)
    posts = relationship('Post', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.fullname!r})'


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('userss.id'))

    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.title!r})'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# user1 = User(name='Bek')
# user2=User(name='Bob')
# session.add(user1)
# session.add(user2)
# session.commit()

# post1 = Post(title='My first day 1', content='My first day content 1', user_id=user1.id)
# post2 = Post(title='My first day 3', content='My first day content 3', user_id=user2.id)

# session.add_all([post2])
# session.commit()


# users = session.query(User).all()
# for user in users:
#     print(f"{user.name}: {user.posts}")

# posts = session.query(Post).all()
# #
# for post in posts:
#     print(f"{post.title}: {post.user}")

# bob = session.query(User).filter(2 == User.id).first()
# session.delete(bob)
# session.commit()

#