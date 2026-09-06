import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

def get_env(target):
    local = os.getenv("USE_LOCAL_DB", "false").lower() == "true"
    return os.getenv(f"LOCAL_{target}") if local else os.getenv(target)

db_pool = pooling.MySQLConnectionPool(
    pool_name="tidb_pool",
    pool_size=3,                           # 最多 3 條連線
    pool_reset_session=True,
    host=get_env("DB_HOST"),
    user=get_env("DB_USER"),
    password=get_env("DB_PASSWORD"),
    database=get_env("DB_NAME"),
    charset=get_env("DB_CHAR")
)

def get_db():
    return db_pool.get_connection()

if __name__ == "__main__":
    try:
        conn = get_db()
        if(conn):
            print("TiDB Cloud 連線成功")
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            print("目前資料表：", cursor.fetchall())
            cursor.close()
            conn.close()
    except Exception as e:
        print("TiDB Cloud 連線失敗，錯誤訊息：", e)