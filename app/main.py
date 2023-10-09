from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import sentry_sdk

from app.web_pages import router_web_pages
from app.auth import router_auth
from app.sockets import router_web_socket


sentry_sdk.init(
    dsn="https://1a6b12e7dbf7418233793cb807de9e53@o4505229726318592.ingest.sentry.io/4505761003864065",
    traces_sample_rate=1.0,
)

app = FastAPI(
    title='Our first app',
    description='we are champions',
    version='0.0.1',
    debug=True
)

app.mount('/app/static', StaticFiles(directory='app/static'), name='static')

app.include_router(router_web_pages.router)
app.include_router(router_auth.router)
app.include_router(router_web_socket.router)


@app.get('/')
@app.post('/')
async def main_page() -> dict:
    return {'greeting': 'HELLO'}


@app.get('/{user_name}')
@app.get('/{user_name}/{user_nick}')
async def user_page(user_name: str, user_nick: str = '', limit: int = 10, skip: int = 0) -> dict:
    data = [i for i in range(1000)][skip:][:limit]

    return {'user_name': user_name, 'user_nick': user_nick, 'data': data}