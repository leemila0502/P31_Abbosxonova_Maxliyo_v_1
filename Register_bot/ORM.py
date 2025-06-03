from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Users(Base):
    __tablename__ = 'Registration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, nullable=True, unique=True)
    username = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(30), nullable=True)
    address = Column(String(50), nullable=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(first_name={self.first_name}, email={self.email})"

    @staticmethod
    async def create_or_update_user(data):
        async with SessionLocal() as session:
            result = await session.execute(select(Users).where(Users.chat_id == data['chat_id']))
            user = result.scalar_one_or_none()
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
            else:
                user = Users(**data)
                session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def get_by_chat_id(chat_id):
        async with SessionLocal() as session:
            result = await session.execute(select(Users).where(Users.chat_id == chat_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_all():
        async with SessionLocal() as session:
            result = await session.execute(select(Users.first_name , Users.chat_id))
            return result.all()

    @staticmethod
    async def delete(chat_id):
        async with SessionLocal() as session:
            result = await session.execute(select(Users).where(Users.chat_id == chat_id))
            user = result.scalar_one_or_none()
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False


    # @staticmethod
    # async def update(chat_id, **kwargs):
    #     async with SessionLocal() as session:
    #         result = await session.execute(select(Users).where(Users.chat_id == chat_id))
    #         user = result.scalar_one_or_none()
    #         if user:
    #             for key, value in kwargs.items():
    #                 if hasattr(user, key):
    #                     setattr(user, key, value)
    #             await session.commit()
    #             return True
    #         return False


    @staticmethod
    async def update(chat_id,**kwargs):
        async with SessionLocal() as session:
            result=await session.execute(select(Users).where(Users.chat_id==chat_id))
            user= result.scalar_one_or_none()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)

                await session.commit()
                return True
            return False


    @staticmethod
    async def add_user(**kwargs):
        async with SessionLocal() as session:
            await session.add(**kwargs)
            await session.commit()


# ASYNC METADATA CREATE
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# p1=Users(id=1,chat_id=0,username='Lee Mila',phone="933977090",email="Mila@gmail.com",address="Chilonzor",first_name='Mila',last_name='Lee')
# session.add(p1)
# session.commit()
