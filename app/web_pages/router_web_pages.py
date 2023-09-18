from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

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


@router.post('/search')
@router.get('/menu')
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
        'user': user
    }

    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )


@router.get('/about-us')
async def about_us(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Про нас',
        'user': user,
    }

    return templates.TemplateResponse(
        'about_us.html',
        context=context,
    )


@router.get('/map')
async def map(request: Request):
    context = {
        'request': request,
        'title': 'Карта проїзду',

    }

    return templates.TemplateResponse(
        'map.html',
        context=context,
    )


@router.get('/message')
async def message(request: Request):
    context = {
        'request': request,
        'title': 'Написати для всіх повідомлення',
    }

    return templates.TemplateResponse(
        'message_to_all.html',
        context=context,
    )


@router.get('/register')
@router.post('/register')
async def register(request: Request):
    context = {
        'request': request,
        'title': 'Реєстрація',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
    }

    return templates.TemplateResponse(
        'register.html',
        context=context,
    )

@router.post('/register-final')
async def register_final(request: Request,
                         name: str = Form(),
                         login: EmailStr = Form(),
                         notes: str = Form(default=''),
                         password: str = Form()):
    is_login_already_used = await dao.get_user_by_login(login)
    if is_login_already_used:
        context = {
            'request': request,
            'title': 'Помилка користувача',
            'content': f'Користувач {login} уже існує',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    hashed_password = await AuthHandler.get_password_hash(password)
    user_data = await dao.create_user(
        name=name,
        login=login,
        password=hashed_password,
        notes=notes,
    )
    token = await AuthHandler.encode_token(user_data[0])
    context = {
        'request': request,
        'title': 'Про нас',
        'menu': menu_data.menu,
        'user': user_data,
    }
    template_response = templates.TemplateResponse(
        'menu.html',
        context=context,
    )
    template_response.set_cookie(key='token', value=token, httponly=True)
    return template_response

