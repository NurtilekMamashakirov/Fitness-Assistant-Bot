from app.database.models import async_session, Gender
from app.database.models import User
from sqlalchemy import select


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
