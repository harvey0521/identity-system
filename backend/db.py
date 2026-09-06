import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

def get_env(target):
    local = os.getenv("USE_LOCAL_DB", "false").lower() == "true"
    return os.getenv(f"LOCAL_{target}") if local else os.getenv(target)

db_pool = pooling.MySQLConnectionPool(
    pool_name="tidb_pool",
    pool_size=3,                           # 免費方案開 2~3 個連線即可
    pool_reset_session=True,
    host=get_env("DB_HOST"),    # 主機位置，如果你用本地的 MySQL 就是 localhost
    user=get_env("DB_USER"),    # 你的 MySQL 帳號
    password=get_env("DB_PASSWORD"),    # 你的 MySQL 密碼
    database=get_env("DB_NAME"),    # 你的資料庫名稱
    charset=get_env("DB_CHAR")  # 避免中文亂碼
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