from enum import Enum


class RoleUser(str, Enum):
    ADMIN = "ADMIN"
    User = "USER"
