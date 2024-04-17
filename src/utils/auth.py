"""Auth user"""
import json
import logging
from functools import wraps
from jwt import JWT as jwt
from google.auth.transport import Request
from google.auth.transport import Request

from src.configs.constants import UserConstant, MasterConstants
from src.configs.env import get_settings
from src.configs.error_constant import ErrorMessage
from src.configs.redis_constant import RedisKey, RedisExp
from src.exceptions.errors.generic import Unauthenticated, UnauthenticatedForbidden
from src.lib.redis import redis_cache
from src.services.user.controller import UserController, user_details_context


config = get_settings()

class Auth:
    """Auth"""

    @classmethod
    def authenticate_user(cls, func):
        """Authenticate user"""
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            await redis_cache.init_cache()
            if config.env != "local":
                if "authorization" in request.headers and request.headers["authorization"]:
                    token = request.headers["authorization"]
                    email = jwt.decode(
                        token,
                        algorithms="RS256",
                        options={"verify_signature": False},
                    )["sub"]
                    email = email.lower()
                elif "header-email" in request.headers and request.headers["header-email"]:
                    email = request.headers["header-email"]
            else:
                email = MasterConstants.DEFAULT_USER
            # raise Unauthenticated(message=ErrorMessage.AUTH_HEADER_ERROR)

            redis_data = await redis_cache.get(key=RedisKey.USER_EMAIL.format(email=email))
            if redis_data:
                user_details_context.set(json.loads(redis_data))
                return await func(request, *args, **kwargs)

            user_details = await UserController.get_by_email_and_id(emails=[email])
            if not user_details:
                logging.error("authenticate_user - Invalid User")
                raise UnauthenticatedForbidden(message=ErrorMessage.UNAUTHORIZED_USER)

            if not user_details or user_details.status == False:
                raise Unauthenticated(message=ErrorMessage.USER_ONBOARDING_ERROR)
            await redis_cache.set(
                key=RedisKey.USER_EMAIL.format(email=email),
                value=json.dumps(user_details.data.dict()),
                ex=RedisExp.USER_EMAIL,
            )
            user_details_context.set(user_details.data.dict())
            return await func(request, *args, **kwargs)

        return wrapper

    @classmethod
    def authorize_user(cls, func):
        """Authorize user"""
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if "authorization" in request.headers and request.headers["authorization"]:
                token = request.headers["authorization"]
                email = jwt.decode(
                    token,
                    algorithms="RS256",
                    options={"verify_signature": False},
                )["sub"]
                email = email.lower()
                if "header-email" in request.headers and request.headers["header-email"]:
                    email = request.headers["header-email"]
            else:
                email = MasterConstants.DEFAULT_USER
            redis_data = await redis_cache.get(key=RedisKey.USER_EMAIL.format(email=email))
            if redis_data:

                return await func(request, *args, **kwargs)
            raise UnauthenticatedForbidden(message=ErrorMessage.UNAUTHORIZED_REQUEST)

        return wrapper

    @classmethod
    def authorize_admin(cls, func):
        """Authorize admin"""

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if "authorization" in request.headers and request.headers["authorization"]:
                token = request.headers["authorization"]
                email = jwt.decode(
                    token,
                    algorithms="RS256",
                    options={"verify_signature": False},
                )["sub"]
                email = email.lower()
                if "header-email" in request.headers and request.headers["header-email"]:
                    email = request.headers["header-email"]
            else:
                email = MasterConstants.DEFAULT_USER
            redis_data = await redis_cache.get(key=RedisKey.USER_EMAIL.format(email=email))
            if redis_data:
                data = json.loads(redis_data)
                if data.get("role_id") == UserConstant.Role.ADMIN:
                    return await func(request, *args, **kwargs)
            raise UnauthenticatedForbidden(message=ErrorMessage.UNAUTHORIZED_REQUEST)

        return wrapper


