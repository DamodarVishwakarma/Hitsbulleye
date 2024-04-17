"""model file for section"""
from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.master.test.schema.section import SectionSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class SectionModel:
    """Section model"""

    @classmethod
    def create(cls, **kw):
        """function to create user auth"""
        obj = SectionSchema(**kw)
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
        obj = (db.query(SectionSchema).filter(SectionSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime()
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_section(_id=_id)

    @classmethod
    def get_section(cls, _id: int = None, status: bool = True, name_key: str = None, is_all: bool = False, limit: int = None):
        """method to get area by id"""
        query = db.query(SectionSchema)
        if _id:
            query = query.filter(SectionSchema.id == _id)
        if name_key and is_all:
            query = query.filter(SectionSchema.name_key.ilike(f"%{name_key}%"))
        elif name_key:
            query = query.filter(SectionSchema.name_key == name_key)
        if status:
            query = query.filter(SectionSchema.status == status)
        if is_all:
            query = query.order_by(SectionSchema.id.desc())
            if limit:
                query = query.limit(limit)
            query = select_all(query)
        else:
            query = select_first(query)
        return query
