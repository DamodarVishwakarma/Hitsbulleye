"""controller file for user auth"""
import hashlib
from contextvars import ContextVar
from typing import List
from src.configs.error_constant import ErrorMessage
from src.exceptions.errors.generic import EntityException
from src.services.user.model import UserAuthModel
from src.services.user.serializer import (
    UserCommonInBound, UserFinalOutbound, UserOutbound, UserAppOutBound,
)
from src.utils.time import get_current_datetime


user_details_context: ContextVar[UserAppOutBound] = ContextVar("user_details")



class UserController:
    """controller for user"""

    @classmethod
    async def save(cls, payload: UserCommonInBound):
        """function to save user"""
        payload_dict = payload.dict(exclude_unset=True, exclude_none=True)
        emails = [payload.email]
        if payload.login_email:
            emails.extend(payload.login_email)
        emails = list(set(emails))
        user_data = UserAuthModel.get_user_data(emails=emails)
        if user_data:
            raise EntityException(message=ErrorMessage.RECORD_ALREADY_EXISTS)
        password = payload_dict.pop('password').encode() if "password" in payload_dict else None
        password_new = hashlib.md5(password).hexdigest() if password else None
        login_emails = [email.lower() for email in payload_dict["login_email"]] if payload_dict.get("login_email") else []
        payload_dict["email"] = payload_dict.get("email").lower()
        payload_dict["password"] = password_new
        payload_dict["login_email"] = list(set(login_emails))
        payload_dict["last_login"] = get_current_datetime(return_string=False)
        data = UserAuthModel.create(**payload_dict)
        return await cls.get_by_email_and_id(_id=data.id)

    @classmethod
    async def get_by_email_and_id(cls, emails: List[str] = None, _id: int = None):
        """get user by id"""
        user_data = UserAuthModel.get_user_data(emails=emails, _id=_id)
        if not user_data or not user_data.status:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("user"))
        response = UserOutbound(
            id=user_data.id,
            email=user_data.email,
            name=user_data.name,
            login_emails=user_data.login_email,
            user_id=user_data.user_id,
            role_id=user_data.role_id
        )
        return UserFinalOutbound(data=response)
