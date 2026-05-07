from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    items: list
    cursor: str | None = None
    has_more: bool = False
    total: int | None = None


class MessageResponse(BaseModel):
    message: str
