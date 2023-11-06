import asyncio
from requests import Session

from sqlalchemy import Engine, insert, select, update, delete

from database import async_session_maker, engine
from models import User, Recipe

# table User
async def create_user(
        name: str,
        surname: str,
        login: str,
        password: str,

):
    async with async_session_maker() as session:
        query = insert(User).values(
            name=name,
            surname=surname,
            login=login,
            password=password,
        ).returning(User.id, User.login, User.name)
        # print(query)
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
        # print(query)
        result = await session.execute(query)
        # print(result.first())
        # print(result.scalar_one_or_none())
        return result.scalar_one_or_none()


async def get_user_by_login(user_login: str):
    async with async_session_maker() as session:
        query = select(User).filter_by(login=user_login)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def update_user(user_id: int, name: str, surname: str, login: str, password: str):
    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(name=name, surname=surname, login=login, password=password)
        # print(query)
        await session.execute(query)
        await session.commit()

async def get_user_password_by_user_id(user_id: str):
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none().password

async def delete_user(user_id: int):
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        # print(query)
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

# table Recipe
async def create_recipe(

    user_id:int,
    recipe_title:str,
    recipe_text:str

):
    async with async_session_maker() as session:
        query = insert(Recipe).values(
            user_id=user_id,
            recipe_title=recipe_title,
            recipe_text=recipe_text,
        ).returning(Recipe.user_id, Recipe.recipe_title, Recipe.recipe_text)
        # print(query)
        data = await session.execute(query)
        await session.commit()
        return tuple(data)[0]

async def fetch_recipes():
    async with async_session_maker() as session:
        query = select(Recipe)
        result = await session.execute(query)
        return result.scalars().all()
    
async def fetch_recipes_by_user_id(user_id):
    async with async_session_maker() as session:
        query = select(Recipe).filter_by(user_id=user_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    
async def get_recipe_by_title(recipe_title: str):
    async with async_session_maker() as session:
        query = select(Recipe).filter_by(recipe_title=recipe_title)
        result = await session.execute(query)
        return result.scalar_one_or_none()



async def main():
    # await asyncio.gather(
    #     create_user(
    #         name='name1',
    #         login='login2',
    #         password='password1',
    #         notes='*'*200
    #     )
    # )
    # print(await asyncio.gather(fetch_users()))
    
    
    # async def testt():
    #     print(await fetch_recipes())
    
    
    



    # await asyncio.gather(get_user_by_id(3))
    # await asyncio.gather(update_user(222))


    # await create_recipe(
    #     user_id=6, recipe_title='new recipe60', recipe_text='How to cook somethinlklg4'

    # )




    # print(await fetch_recipes())
    # a = await get_recipe_by_title('new recipe2')
    # print(a)
    # print(a.id)

    list_of_recipes = await fetch_recipes_by_user_id(1)
    for dict in list_of_recipes:
        print(dict)
        if dict.id == 13:
            print(dict.id)
    # print()
    # print(await fetch_recipes())

# asyncio.gather(main())



# {'id': 1, 'user_id': 1, 'image_name': None, 'recipe_text': 'How to cook something', 'recipe_title': 'new recipe'}
