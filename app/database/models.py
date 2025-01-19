from datetime import datetime

from sqlalchemy import BigInteger, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    age: Mapped[int] = mapped_column()
    sex: Mapped[str] = mapped_column(String(10))
    weight: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    aim: Mapped[str] = mapped_column(String(800))


class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    type: Mapped[str] = mapped_column(String(20))
    time = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[int] = mapped_column()


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    text: Mapped[str] = mapped_column(String(800))
    time = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
