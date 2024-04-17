"""model file for section"""
from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.master.test.schema.test_direction import TestDirectionSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class TestDirectionModel:
    """Section model"""

    @classmethod
    def create(cls, **kw):
        """function to create test direction"""
        obj = TestDirectionSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        obj.created_by = user_details_context.get().get("id")
        obj.updated_by = user_details_context.get().get("id")
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method patch test direction data"""
        obj = (db.query(TestDirectionSchema).filter(TestDirectionSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime()
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_by_id(_id=_id)

    @classmethod
    def get_by_id(cls, _id: int = None, status: bool = True, domain_id: int = None, test_type: int = None):
        """method to get test direction by id"""
        query = db.query(TestDirectionSchema)
        if _id:
            query = query.filter(TestDirectionSchema.id == _id)
        if domain_id:
            query = query.filter(TestDirectionSchema.domain_id == domain_id)
        if test_type:
            query = query.filter(TestDirectionSchema.test_type == test_type)
        if status:
            query = query.filter(TestDirectionSchema.status == status)
        if not _id:
            query = select_all(query)
        else:
            query = select_first(query)
        return query
