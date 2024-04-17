"""common file for commonly used function"""
import json
import re
from typing import List

from src.configs.redis_constant import RedisKey
from src.lib.redis import redis_cache
from src.services.user.model import UserAuthModel
from src.utils.common_serializer import UserOutbound


def name_key_serializer(name: str):
    """Function to remove all characters except letters and numbers"""
    if name is not None:
        return re.sub("[\W_]+", "", name.lower())
    else:
        return None


def get_user_outbound(_id: int = None, emails: List[str] = None):
    """get user outbound"""
    user_data = UserAuthModel.get_user_data(_id=_id, emails=emails)
    data = None
    if user_data:
        data = UserOutbound(
            id=user_data.id,
            name=user_data.name,
            email=user_data.email,
            user_id=user_data.user_id,
            role_id=user_data.role_id,
        )
    return data
