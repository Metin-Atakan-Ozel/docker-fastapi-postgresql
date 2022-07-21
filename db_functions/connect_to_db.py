import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import sys

try:
    conn = psycopg2.connect(database="movie", user='postgres', password='password', host='db', port='5432')
except Exception as error:
    print('Unable to connect to Database! >> {}',error)

    sys.exit(1)

conn.autocommit = True
cursor = conn.cursor(cursor_factory=RealDictCursor)