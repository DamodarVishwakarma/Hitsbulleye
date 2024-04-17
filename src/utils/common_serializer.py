"""common serializer file"""
from typing import Optional, Any
from pydantic import BaseModel


class Page(BaseModel):
    """paging"""
    page_size: Optional[int] = 0
    page_number: Optional[int] = 0
    num_pages: Optional[int] = 0
    total_result: Optional[int] = 0


class SuccessResponse(BaseModel):
    """Success Response"""
    status: Optional[int] = 200
    column_data: Optional[Any]
    message: str = "data save successfully"
    page: Optional[Page]
    data: Optional[Any]


class SuccessResponsePartial(BaseModel):
    """Success Response"""
    status: Optional[int] = 200
    message: str = "data save successfully"
    page: Optional[Page]
    data: Optional[Any]


class UserOutbound(BaseModel):
    """user outbound"""
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    user_id: Optional[int]
    role_id: Optional[int]
