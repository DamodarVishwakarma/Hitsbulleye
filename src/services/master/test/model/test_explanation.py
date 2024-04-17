"""model file for test explanation"""
from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.master.test.schema.test_explanation import TestExplanationSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class TestExplanationModel:
    """Test Explanation model"""

    @classmethod
    def create(cls, **kw):
        """function to create test explanation"""
        obj = TestExplanationSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        obj.created_by = user_details_context.get().get("id")
        obj.updated_by = user_details_context.get().get("id")
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method patch test explanation data"""
        obj = (db.query(TestExplanationSchema).filter(TestExplanationSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime()
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_by_id(_id=_id)

    @classmethod
    def get_by_id(cls, _id: int = None, status: bool = True, test_type: int = None):
        """method to get test direction by id"""
        query = db.query(TestExplanationSchema)
        if _id:
            query = query.filter(TestExplanationSchema.id == _id)
        if test_type:
            query = query.filter(TestExplanationSchema.test_type == test_type)
        if status:
            query = query.filter(TestExplanationSchema.status == status)
        if not _id:
            query = select_all(query)
        else:
            query = select_first(query)
        return query
