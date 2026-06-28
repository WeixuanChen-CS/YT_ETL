from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyscopg2.extras import RealDictCursor

table = "yt_api"

def get_con_cursor():
    hook = PostgresHook(postgres_conn_id='postgres_db_yt_elt', database='elt_db')
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return cur, conn

def close_conn_cursor(cur, conn):
    cur.close()
    conn.close()

def create_schema(schema):
    con, cur = get_con_cursor()
    schema_aql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    cur.execute(schema_aql)
    con.commit()

    close_conn_cursor(cur, con)

def create_table(schema):
    cur, con = get_con_cursor()
    
    if schema == "staging":
        table_aql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "UPload_Date" TIMESTAMP NOT NULL,
                    "DURATION" VARCHAR(20) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT,
                );
            """
    else:
        table_aql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "UPload_Date" TIMESTAMP NOT NULL,
                    "DURATION" TIME NOT NULL,
                    "Video_Type" VARCHAR(10) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT,
                );
            """
    cur.execute(table_aql)
    con.commit()

    close_conn_cursor(cur, con)

def get_video_ids(cur, schema):

    cur.execute(f"""SELECT \"Video_ID\" FROM {schema}.{table};""")
    ids = cur.fetchall()

    video_ids = [row["Video_ID"] for row in ids]

    return video_ids