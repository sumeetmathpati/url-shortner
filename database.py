from flask import g
import psycopg2
from psycopg2.extras import DictCursor

def connect_db():
    conn = psycopg2.connect('postgres://epiqyfxlurqhrg:31bb627e0b611243bde68e6a095fa6c34f0ba9d9ca298c71f49dc06b29552f1f@ec2-52-1-95-247.compute-1.amazonaws.com:5432/dfum13t49qh7st', cursor_factory=DictCursor)
    conn.autocommit = True
    sql = conn.cursor()
    return conn, sql

def get_db():

    db = connect_db()
    
    if not hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn = db[0]
    
    if not hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur = db[1]

    return g.postgres_db_cur

