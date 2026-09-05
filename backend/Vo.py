from dataclasses import dataclass


@dataclass
class UserVo:
    id: str
    name: str
    phone: str
    address: str
    other: str
