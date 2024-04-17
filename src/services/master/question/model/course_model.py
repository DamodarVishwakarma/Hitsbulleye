"""model file for Course"""
from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.master.question.schema.course_schema import CourseSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class CourseModel:
    """User Auth model"""

    @classmethod
    def create(cls, **kw):
        """function to create user auth"""
        obj = CourseSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        obj.created_by = user_details_context.get().get("id")
        obj.updated_by = user_details_context.get().get("id")
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method patch course data"""
        obj = (db.query(CourseSchema).filter(CourseSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime()
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_by_id(_id=_id)

    @classmethod
    def get_by_id(cls, _id: int = None, status: bool = None, name_key: str = None):
        """method to get area by id"""
        query = db.query(CourseSchema)
        if _id:
            query = query.filter(CourseSchema.id == _id)
        if name_key:
            query = query.filter(CourseSchema.name_key == name_key)
        if status:
            query = query.filter(CourseSchema.status == status)
        query = select_first(query)
        return query

    @classmethod
    def get_list(cls, name_key: str = None):
        """method to get area list"""
        query = db.query(CourseSchema).filter(CourseSchema.status == True)
        if name_key:
            query = query.filter(CourseSchema.name_key.ilike(name_key))
        query = select_all(query)
        return query
