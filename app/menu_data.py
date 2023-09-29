from enum import Enum


class Categories(Enum):
    CHEESE = 'з сиром'
    MEAT = 'з мясом'
    SEAFOOD = 'з морепродуктами'


menu = [
    {
        'title': 'Карбонара',
        'image': 'image(1).png',
        'price': 220,
        'categories': [Categories.CHEESE.value, Categories.MEAT.value]
    },
    {
        'title': 'Пепероні',
        'image': 'image(2).png',
        'price': 180,
        'categories': [Categories.CHEESE.value, Categories.MEAT.value]
    },
    {
        'title': 'Барбекю',
        'image': 'image(3).png',
        'price': 220,
        'categories': [Categories.MEAT.value]
    },
    {
        'title': 'Пепероні з копченим мясом',
        'image': 'image(4).png',
        'price': 300,
        'categories': [Categories.CHEESE.value, Categories.MEAT.value, Categories.SEAFOOD.value]
    },
]