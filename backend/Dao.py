from db import get_db
from Vo import UserVo
import logging


# 取得所有資料
def get_all_dao():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        logging.debug(rows)

        result = []

        for i in rows:
            users = UserVo(
                id=i["id"],
                name=i["name"],
                phone=i["phone"],
                address=i["address"],
                other=i["other"],
            )
            result.append(users)
        logging.debug(result)

        logging.info("資料取得成功")
        return result
    finally:
        cursor.close()
        conn.close()
        logging.info("資料庫連線已關閉")


# 查詢
def get_dao(id: str):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))

        row = cursor.fetchone()
        logging.debug(f"資料庫查詢結果：{row}")

        if row:
            logging.info(f"查詢成功、查到證號 {id} 的資料")

            result = UserVo(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                address=row["address"],
                other=row["other"],
            )
            return result
        else:
            logging.warning(f"查詢失敗、查無證號 {id} 的資料")
            return None
    finally:
        cursor.close()
        conn.close()
        logging.info("資料庫連線已關閉")


# 新增
def post_dao(data: dict):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (id, name, phone, address, other) VALUES (%s, %s, %s, %s, %s)",
            (data["id"], data["name"], data["phone"], data["address"], data["other"]),
        )

        conn.commit()  # 寫入資料庫
        logging.info("新增成功")
        return data
    finally:
        cursor.close()
        conn.close()
        logging.info("資料庫連線已關閉")


# 修改
def put_dao(id: str, data: dict):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET name=%s, phone=%s, address=%s, other=%s WHERE id=%s",
            (data["name"], data["phone"], data["address"], data["other"], id),
        )
        conn.commit()

        affected = cursor.rowcount  # 會回傳 1（代表有 1 筆被更新）

        logging.debug(f"有 {affected} 筆被更新")

        if affected:
            logging.info(f"修改成功、已修改證號 {id} 的資料")
            return True
        else:
            logging.warning(f"修改失敗、查無此 {id} 證號")
        return False
    finally:
        cursor.close()
        conn.close()
        logging.info("資料庫連線已關閉")


# 刪除
def delete_dao(id: str):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        conn.commit()

        affected = cursor.rowcount  # 會回傳 1（代表有 1 筆被更新）

        logging.debug(f"有 {affected} 筆被更新")

        if affected:
            logging.info(f"刪除成功、已刪除證號 {id} 的資料")
            return True
        else:
            logging.warning(f"刪除失敗、查無此 {id} 證號")
            return False
    finally:
        cursor.close()
        conn.close()
        logging.info("資料庫連線已關閉")


# 查詢 id 是否存在
def has_id_dao(id: str):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        row = cursor.fetchone()

        if row:
            logging.warning(f"新增失敗、此 {id} 身分證資料已存在")

            id_record = UserVo(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                address=row["address"],
                other=row["other"],
            )

            return id_record

        return False
    finally:
        cursor.close()
        conn.close()
        logging.info("資料庫連線已關閉")
