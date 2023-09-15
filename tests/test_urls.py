import http


async def test_main_page_get(client):
    responce = client.get('/')
    assert responce.status_code == http.HTTPStatus.OK
    assert responce.json() == {'greeting': 'HELLO'}


async def test_main_page_post(client):
    responce = client.post('/')
    assert responce.status_code == http.HTTPStatus.OK
    assert responce.json() == {'greeting': 'HELLO'}