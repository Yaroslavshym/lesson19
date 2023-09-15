import asyncio

from sqlalchemy import insert, select, update, delete

from database import async_session_maker
from models import User, Order


async def create_user(
        name: str,
        login: str,
        password: str,
        notes: str = '',
        is_conflict: bool = False,
):
    async with async_session_maker() as session:
        query = insert(User).values(
            name=name,
            login=login,
            password=password,
            notes=notes,
            is_conflict=is_conflict,
        ).returning(User.id, User.login)
        print(query)
        data = await session.execute(query)
        await session.commit()
        return tuple(data)[0]


async def fetch_users(skip: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)
        # print(type(result.scalars().all()[0]))
        # print(result.scalars().all()[0].__dict__)
        return result.scalars().all()


async def get_user_by_id(user_id: int):
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        print(query)
        result = await session.execute(query)
        # print(result.first())
        # print(result.scalar_one_or_none())
        return result.scalar_one_or_none()


async def get_user_by_login(user_login: str):
    async with async_session_maker() as session:
        query = select(User).filter_by(login=user_login)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def update_user(user_id: int):
    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(name='Vasja')
        print(query)
        await session.execute(query)
        await session.commit()


async def delete_user(user_id: int):
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        print(query)
        await session.execute(query)
        await session.commit()


# async def main():
#     # await asyncio.gather(
#     #     create_user(
#     #         name='name1',
#     #         login='login2',
#     #         password='password1',
#     #         notes='*'*200
#     #     )
#     # )
#     # await asyncio.gather(fetch_users())
#     # await asyncio.gather(get_user_by_id(3))
#     # await asyncio.gather(update_user(222))
#     await asyncio.gather(delete_user(2))
#
# asyncio.run(main())