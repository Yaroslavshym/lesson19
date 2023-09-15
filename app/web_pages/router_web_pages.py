from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from app import menu_data


router = APIRouter(
    prefix='/web',
    tags=['menu', 'landing'],
)

templates = Jinja2Templates(directory='app\\templates')


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
async def get_menu(request: Request, dish_name: str = Form(None)):
    filtered_menu = []
    if dish_name:
        for dish in menu_data.menu:
            if dish_name.lower() in dish['title'].lower():
                filtered_menu.append(dish)

    context = {
        'request': request,
        'title': f'Результати пошуку за {dish_name}' if dish_name else 'Наше меню',
        'menu': filtered_menu if dish_name else menu_data.menu,
        'username': 'ljdvhgjkdfkg',
        'is_admin': False
    }

    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )


@router.get('/about-us')
async def about_us(request: Request):
    context = {
        'request': request,
        'title': 'Про нас',
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