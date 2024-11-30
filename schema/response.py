from dataclasses import dataclass
from typing import Optional, Generic

from typing_extensions import TypeVar

T = TypeVar("T")


@dataclass
class Response(Generic[T]):
    data: Optional[T]
    message: str
    code: int
