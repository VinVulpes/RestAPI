'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import orders as settings

# DATABASE_NAME = ''
def get_engine()
'''
import psycopg2

con = psycopg2.connect(
    database="database_test",
    user="user_test",
    password="qwerty",
    host="localhost",
    port="5432"
  )
cur = con.cursor()
def connect_db_pg():

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders( 
      id serial constraint order_pk PRIMARY KEY,
      order_name text NOT NULL,
      start_date timestamptz
    );
''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks(
      id serial constraint task_pk PRIMARY KEY,
      order_id integer constraint task_fk REFERENCES orders ON DELETE CASCADE,
      duration integer NOT NULL,
      resource integer NOT NULL,
      pred integer ARRAY
    );
''')
    con.commit()
    return con




'''
CREATE TABLE IF NOT EXISTS ORDERS
      (order_name char(50) PRIMARY KEY NOT NULL,
      start_date char (50));

create table if not exists task(
    id serial constraint task_pk PRIMARY KEY,
    order_name text not null,
    start_date timestamptz
);

create table if not exists work(
    id  serial constraint work_pk PRIMARY KEY,
    task_id integer constraint work_fk REFERENCES task ON DELETE CASCADE,
    duration integer not null,
    resource integer not null,
    parent_id integer
);
'''
