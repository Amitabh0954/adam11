from typing import TypedDict, Optional

class Category(TypedDict):
    id: int
    name: str
    parent_id: Optional[int]