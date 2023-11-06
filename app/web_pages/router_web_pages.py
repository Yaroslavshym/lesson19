from fastapi import APIRouter, Request, Form, HTTPException, status, Depends, Response, UploadFile, File
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
import shutil
import requests

from app.auth.FA2 import make_otp
from app import menu_data
from app.auth.auth_lib import AuthHandler, AuthLibrary
from app.auth import dependencies


import dao

import settings


router = APIRouter(
    prefix='/web',
    tags=['menu', 'landing'],
)

templates = Jinja2Templates(directory='app//templates')


# @router.get('/')
# async def get_main_page(request: Request):
#     context = {
#         'request': request,
#     }
#
#     return templates.TemplateResponse(
#         'base.html',
#         context=context,
#     )


# @router.get('/menu')
# async def get_menu(request: Request):
#     context = {
#         'request': request,
#         'title': 'Наше меню',
#         'menu': menu_data.menu,
#     }
#
#     return templates.TemplateResponse(
#         'menu.html',
#         context=context,
#     )


# @router.post('/search')
# @router.get('/menu')
async def get_menu(request: Request, dish_name: str = Form(None), user=Depends(dependencies.get_current_user_optional)):
    filtered_menu = []


    if dish_name:
        for dish in menu_data.menu:
            if dish_name.lower() in dish['title'].lower():
                filtered_menu.append(dish)

    context = {
        'request': request,
        'title': f'Результати пошуку за {dish_name}' if dish_name else 'Наше меню',
        'menu': filtered_menu if dish_name else menu_data.menu,
        'user': user,
        'categories': menu_data.Categories
    }

    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )


# @router.get('/about-us')
async def about_us(request: Request, user=Depends(dependencies.get_current_user_optional)):

    context = {
        'request': request,
        'title': 'Abou us',
        'user': user,
    }
    
    return templates.TemplateResponse(
        'about_us.html',
        context=context,
    )


# @router.get('/map')
async def map_drive(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Map',
        'user': user,

    }

    return templates.TemplateResponse(
        'map.html',
        context=context,
    )


# @router.get('/message')
async def message(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Написати для всіх повідомлення',
        'user': user,
    }

    return templates.TemplateResponse(
        'message_to_all.html',
        context=context,
    )


@router.get('/register')
@router.post('/register')
async def register(request: Request):

    make_otp()
    context = {
        'request': request,
        'title': 'Sign up',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
    }

    return templates.TemplateResponse(
        'register.html',
        context=context,
    )


@router.post('/register-final')
async def register_final(request: Request,
                         user=Depends(dependencies.get_current_user_optional),
                         name: str = Form(),
                         surname: str = Form(),
                         login: EmailStr = Form(),
                         password: str = Form(),
                        #  fa2: str = Form(),
                         ):
    
    is_login_already_used = await dao.get_user_by_login(login)
    if is_login_already_used:
        context = {
            'request': request,
            'title': 'Error',
            'content': f'User {login} already exists',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    hashed_password = await AuthHandler.get_password_hash(password)
    user_data = await dao.create_user(
        name=name,
        surname=surname,
        login=login,
        password=hashed_password,
    )
    
    # context = {
    #     'request': request,
    #     'title': 'Про нас',
    #     'menu': menu_data.menu,
    #     'user': user_data,
    #     'categories': menu_data.Categories
    # }
    # template_response = templates.TemplateResponse(
    #     'menu.html',
    #     context=context,
    # )
    # template_response.set_cookie(key='token', value=token, httponly=True)
    token = await AuthHandler.encode_token(user_data[0])





    list_of_recipes = await dao.fetch_recipes()
    context = {

        'request': request,
        'title': 'Recipes',
        'user': user,

        'recipes': list_of_recipes,
    }
    response =  templates.TemplateResponse(
        'recipes.html',
        context=context,
    )
    response.set_cookie(key='token', value=token, httponly=True)
    
    return response



@router.get('/login')
async def login(request: Request):
    context = {
        'request': request,
        'title': 'Ввійти',
    }
    return templates.TemplateResponse(
        'login.html',
        context=context,
    )


@router.post('/login-final')
async def login(request: Request, login: EmailStr = Form(), password: str = Form()):
    user = await AuthLibrary.authenticate_user(login=login, password=password)
    token = await AuthHandler.encode_token(user.id)
    

    list_of_recipes = await dao.fetch_recipes()
    context = {

        'request': request,
        'title': 'Recipes',
        'user': user,

        'recipes': list_of_recipes,
    }
    response =  templates.TemplateResponse(
        'recipes.html',
        context=context,
    )
    response.set_cookie(key='token', value=token, httponly=True)
    return response


@router.post('/logout')
@router.get('/logout')
async def logout(request: Request, response: Response, user=Depends(dependencies.get_current_user_optional)):

    list_of_recipes = await dao.fetch_recipes()
    context = {

        'request': request,
        'title': 'Recipes',
        'user': user,

        'recipes': list_of_recipes,
    }
    result = templates.TemplateResponse(
        'recipes.html',
        context=context,
    )
    result.delete_cookie('token')
    return result


# @router.get('/by_category/{category_name}')
async def by_category(category_name: str, request: Request, user=Depends(dependencies.get_current_user_optional)):
    menu = [menu for menu in menu_data.menu if category_name in menu['categories']]

    context = {
        'request': request,
        'title': f'Наше меню - результати пошуку по категорії {category_name}',
        'menu': menu,
        'user': user,
        'categories': menu_data.Categories
    }
    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )

# @router.post('/upload')
# async def upload_file(file: UploadFile = File(...)):
    
#     with open('test.png', "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     print(file)
#     return 1

@router.get('/add_recipe')
async def add_recipe(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Create recipe',
        'user': user,
    }
    return templates.TemplateResponse(
        'add_recipe.html',
        context=context,
    )

@router.post('/add_recipe_final')
async def add_recipe_final(request: Request,

                           recipe_text: str = Form(),
                           recipe_title: str = Form(),
                           user=dependencies.get_current_user_optional,
                           user_id=Depends(dependencies.get_current_user_id)
    ):


    is_recipe_title_already_used = await dao.get_recipe_by_title(recipe_title)
    if is_recipe_title_already_used:
        context = {
            'request': request,
            'title': 'Error',
            'user': user,
            'content': f'Recipe with title: "{recipe_title}" already exist.',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    await dao.create_recipe(user_id=user_id, 
                            recipe_title=recipe_title, 
                            recipe_text=recipe_text)
    list_of_user_recipes = await dao.fetch_recipes_by_user_id(user_id)
    context = {
        'request': request,
        'title': 'Your recipes',
        'user': user,
        'recipes': list_of_user_recipes,
    }
    return templates.TemplateResponse(
        'your_recipes.html',
        context=context,
    )


@router.get('/your_recipes')
async def get_recipe(request: Request, user=Depends(dependencies.get_current_user_optional), user_id=Depends(dependencies.get_current_user_id)):
    list_of_user_recipes = await dao.fetch_recipes_by_user_id(user_id)
    print(list_of_user_recipes, user_id)
    context = {
        'user': user,
        'request': request,
        'title': 'Your recipes',
        'recipes': list_of_user_recipes,
    }
    return templates.TemplateResponse(
        'your_recipes.html',
        context=context,
    )
@router.get('/main')
@router.get('/recipes')
async def get_recipe(request: Request, user=Depends(dependencies.get_current_user_optional)):
    list_of_recipes = await dao.fetch_recipes()
    # new_dict_of_recipes = {}
    # for recipe in list_of_recipes:
    #     user_name = (await dao.get_user_by_id(recipe.user_id)).name
    #     new_dict_of_recipes[f'{recipe.user_id}'] = f'{user_name}'
    # print(new_dict_of_recipes[f"{recipe.user_id}"])
            # <p>{{ new_dict_of_recipes[f"{recipe.user_id}"] }}</p>

        
    context = {

        'request': request,
        'title': 'Recipes',
        'user': user,
        # 'new_dict_of_recipes': new_dict_of_recipes,
        'recipes': list_of_recipes,
    }
    return templates.TemplateResponse(
        'recipes.html',
        context=context,
    )




@router.get('/change_profile_info')
async def change_profile_info(request: Request, user=Depends(dependencies.get_current_user_optional), user_id=Depends(dependencies.get_current_user_id)):

    user_data = await dao.get_user_by_id(user_id)
    context = {
        'request': request,
        'user': user,
        'title': 'Change some account data',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
        'user_data': user_data,

    }

    return templates.TemplateResponse(
        'change_profile_info.html',
        context=context,
    )


@router.post('/change_profile_info_final')
async def change_profile_info(request: Request,
                              name: str = Form(),
                              surname: str = Form(),
                              login: EmailStr = Form(),

                              password: str = Form(default=''),
                              user=Depends(dependencies.get_current_user_optional),
                              
                              user_id=Depends(dependencies.get_current_user_id),
                              ):
    hashed_password = await dao.get_user_password_by_user_id(user_id)
    hashed_password = await AuthHandler.get_password_hash(password)
    await dao.update_user(
    user_id=user_id,
    name=name,
    surname=surname,
    login=login,
    password=hashed_password)
        

    token = await AuthHandler.encode_token(user_id)
    
    list_of_recipes = await dao.fetch_recipes()
    context = {

        'request': request,
        'title': 'Recipes',
        'user': user,

        'recipes': list_of_recipes,
    }
    response=  templates.TemplateResponse(
        'recipes.html',
        context=context,
    )
    response.set_cookie(key='token', value=token, httponly=True)
    return response


@router.get('/change_password')
async def change_password(request: Request, 
                    user=Depends(dependencies.get_current_user_optional)):



    context = {
        'request': request,
        'user': user,
        'title': 'Change some account data',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
        'user_data': user,

    }

    return templates.TemplateResponse(
        'change_password.html',
        context=context,
    )






@router.post('/change_password_final')
async def change_password(request: Request,
                    user=Depends(dependencies.get_current_user_optional),
                    password: str = Form(),
                    newPassword: str = Form()):
    if not (await AuthHandler.verify_password(password, user.password)):
        context = {
            'request': request,
            'title': 'Error',
            'user': user,
            'content': f'Incorrect old password',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE)
    hashed_password = await AuthHandler.get_password_hash(newPassword)

    await dao.update_user(
    user_id=user.id,
    name=user.name,
    surname=user.surname,
    login=user.login,
    password=hashed_password
    )
    list_of_recipes = await dao.fetch_recipes()
    context = {

        'request': request,
        'title': 'Recipes',
        'user': user,
        # 'new_dict_of_recipes': new_dict_of_recipes,
        'recipes': list_of_recipes,
    }
    return templates.TemplateResponse(
        'recipes.html',
        context=context,
    )