"""serializer file for user auth"""
from typing import Optional, List
from pydantic import BaseModel, constr
from src.configs.constants import MasterConstants
from src.utils.common_serializer import SuccessResponsePartial


class UserCommonInBound(BaseModel):
    """serializer for user inbound"""
    email: constr(regex=MasterConstants.EMAIL_REGEX)
    login_email: Optional[List[constr(regex=MasterConstants.EMAIL_REGEX)]]
    password: Optional[str]
    name: Optional[str]
    user_id: Optional[int]


class UserOutbound(BaseModel):
    """serializer for user inbound"""
    id: Optional[int]
    email: Optional[str]
    name: Optional[str]
    login_emails: Optional[List[str]]
    user_id: Optional[int]
    role_id: Optional[int]


class UserFinalOutbound(SuccessResponsePartial):
    """user final outbound"""
    data: Optional[UserOutbound]


class UserAppOutBound(BaseModel):
    """User APP OutBound"""
    id: int
    user_id: Optional[int]
    email: str
    login_email: List[str]
    role_id: int
    status: Optional[int]

    class Config:
        """Config"""
        orm_mode = True
