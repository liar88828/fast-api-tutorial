from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Response:
    data: Optional[Any]
    message: str
    code: int
