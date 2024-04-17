"""model file for area Direction"""
from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.master.question.schema.area_direction import AreaDirectionSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class AreaDirectionModel:
    """User Auth model"""

    @classmethod
    def create(cls, **kw):
        """function to create user auth"""
        obj = AreaDirectionSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        obj.created_by = user_details_context.get().get("id")
        obj.updated_by = user_details_context.get().get("id")
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method patch area direction data"""
        obj = (db.query(AreaDirectionSchema).filter(AreaDirectionSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime()
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_by_id(_id=_id)

    @classmethod
    def get_by_id(cls, _id: int = None, status: bool = True, area_id: int = None):
        """method to get area by id"""
        query = db.query(AreaDirectionSchema)
        if _id:
            query = query.filter(AreaDirectionSchema.id == _id)
        if area_id:
            query = query.filter(AreaDirectionSchema.area_id == area_id)
        if status:
            query = query.filter(AreaDirectionSchema.status == status)
        if not _id:
            query = select_all(query)
        else:
            query = select_first(query)
        return query
