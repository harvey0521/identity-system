from flask import Flask, request, send_from_directory
from flask_cors import CORS
from response import response
from Dao import get_all_dao, get_dao, post_dao, put_dao, delete_dao, has_id_dao
import os
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 設定格式
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(message)s]", "%Y-%m-%d %H:%M:%S"
)

# 建立 log 檔輸出
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(
    f"{log_dir}/app.log",
    mode="w",
    encoding="utf-8",  # 預設就是 mode="a" 加在原檔案後面模式
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 終機端輸出
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",            # Vite 預設本機網址
])

def function():
    pass


conn = function()
print(conn)  # None

# 取所有資料
@app.route("/api/users", methods=["GET"])
def get_all():
    try:
        logging.info("執行取得資料")

        result = get_all_dao()

        return response(True, "資料取得成功", result)

    except Exception as e:
        logging.error(f"資料取得系統異常、錯誤訊息：{e}")
        return response(False, "資料取得系統異常", None)


# 查詢
@app.route("/api/users/<id>", methods=["GET"])
def get(id):
    try:
        logging.info("執行查詢")

        result = get_dao(id)

        if result:
            return response(True, "查詢成功", result)
        else:
            return response(False, "查無資料", None)

    except Exception as e:
        logging.error(f"查詢系統異常、錯誤訊息：{e}")  # f-string 自動轉字串
        return response(False, "查詢系統異常", None)


# 新增
@app.route("/api/users", methods=["POST"])
def post():
    try:
        logging.info("執行新增")

        data = request.json
        logging.debug(data)

        id_record = has_id_dao(data["id"])

        if not id_record:

            result = post_dao(data)

            return response(True, "新增成功", result)
        else:
            return response(False, f"新增失敗、此身分證資料已存在", id_record)

    except Exception as e:
        logging.error(f"新增系統異常、錯誤訊息：{e}")
        return response(False, "新增系統異常", None)


# 修改
@app.route("/api/users/<id>", methods=["PUT"])
def put(id):
    try:
        logging.info("執行修改")

        data = request.json
        logging.debug(data)

        affected = put_dao(id, data)

        if affected:  # 如有筆數被更新
            return response(True, "修改成功", data)
        else:
            return response(False, "修改失敗、查無此證號", None)

    except Exception as e:
        logging.error(f"修改系統異常、錯誤訊息：{e}")
        return response(False, "修改系統異常", None, None)


# 刪除
@app.route("/api/users/<id>", methods=["DELETE"])
def delete(id):
    try:
        logging.info("執行刪除")

        affected = delete_dao(id)

        if affected:
            return response(True, "刪除成功", id)
        else:
            return response(False, "刪除失敗、查無此證號", id)

    except Exception as e:
        logging.error(f"刪除系統異常、錯誤訊息：{e}")
        return response(False, "刪除系統異常", None)


if __name__ == "__main__":
    app.run(debug=True)
