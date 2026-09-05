from dataclasses import dataclass, asdict
from flask import jsonify
from typing import Any, Optional


@dataclass
class Response:
    success: Optional[bool]
    message: str
    data: Optional[Any]


def response(success, message, data):
    resp = Response(success, message, data)
    return jsonify(asdict(resp))  # asdict 轉字典格式
