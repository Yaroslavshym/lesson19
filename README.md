https://www.elephantsql.com/
https://www.pgadmin.org/download/
https://dbeaver.io/download/


pip install python-dotenv

pip install sqlalchemy alembic asyncpg psycopg2 psycopg2-binary


alembic init migration

alembic revision --autogenerate -m 'initial' 

 alembic upgrade head

 alembic downgrade -1


pip install fastapi[all] pytest pytest-asyncio

uvicorn app.main:app --reload --port 8000 

pytest -vs . 

pip install websockets