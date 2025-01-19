from datetime import datetime

from sqlalchemy import select

from app.database.models import User, Message
from app.database.models import async_session, Training


async def set_user(tg_id: int, age: int, sex: str, weight: int, height: int, aim: str) -> None:
    user = await get_user(tg_id)
    async with async_session() as session:
        if not user:
            session.add(User(tg_id=tg_id, age=age, sex=sex, weight=weight, height=height, aim=aim))
            await session.commit()


async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def update_aim(tg_id: int, aim: str) -> None:
    async with async_session() as session:
        user_to_update = await session.scalar(select(User).where(User.tg_id == tg_id))
        user_to_update.aim = aim
        session.add(user_to_update)
        await session.commit()


async def update_age(tg_id: int, age: int) -> None:
    async with async_session() as session:
        user_to_update = await session.scalar(select(User).where(User.tg_id == tg_id))
        user_to_update.age = age
        session.add(user_to_update)
        await session.commit()


async def update_weight(tg_id: int, weight: int) -> None:
    async with async_session() as session:
        user_to_update = await session.scalar(select(User).where(User.tg_id == tg_id))
        user_to_update.weight = weight
        session.add(user_to_update)
        await session.commit()


async def update_height(tg_id: int, height: int) -> None:
    async with async_session() as session:
        user_to_update = await session.scalar(select(User).where(User.tg_id == tg_id))
        user_to_update.height = height
        session.add(user_to_update)
        await session.commit()


async def set_training(tg_id: int, date: str, time: str, type_: str) -> None:
    async with async_session() as session:
        date_time = f"{date} {time}"
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        training = Training(tg_id=tg_id, time=date_time, type=type_, status=1)
        session.add(training)
        await session.commit()


async def get_trainings(tg_id: int) -> list:
    async with async_session() as session:
        trainings = await session.scalars(select(Training).where(Training.tg_id == tg_id).where(Training.status == 1))
    return trainings.all()


async def get_all_trainings() -> list:
    async with async_session() as session:
        trainings = await session.scalars(select(Training).where(Training.status == 1))
    return trainings.all()


async def deactive_training(training_id: int) -> None:
    async with async_session() as session:
        training = await session.scalar(select(Training).where(Training.id == training_id))
        training.status = 0
        session.add(training)
        await session.commit()


async def set_message(tg_id: int, message: str) -> None:
    async with async_session() as session:
        message_to_save = Message(tg_id=tg_id, text=message, time=datetime.now())
        session.add(message_to_save)
        await session.commit()
