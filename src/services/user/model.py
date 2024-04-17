"""model file for user auth"""
from typing import List

from sqlalchemy import or_

from src.db.session import save_new_row, get_db, select_first, update_old_row
from src.services.user.schema import UserAuthSchema
from src.utils.time import get_current_datetime

db = get_db()


class UserAuthModel:
    """User Auth model"""

    @classmethod
    def create(cls, **kw):
        """function to create user auth"""
        obj = UserAuthSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        obj.created_by = 0
        obj.updated_by = 0
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def get_user_data(cls, _id: int = None, emails: List[str] = None, user_id: int = None):
        """method to get user_auth by id"""
        query = db.query(UserAuthSchema).filter(UserAuthSchema.status == True)
        if _id:
            query = query.filter(UserAuthSchema.id == _id)
        if emails:
            query = query.filter(or_(UserAuthSchema.login_email.overlap(emails), UserAuthSchema.email.in_(emails)))
        if user_id:
            query = query.filter(UserAuthSchema.user_id == user_id)
        query = select_first(query)
        return query
