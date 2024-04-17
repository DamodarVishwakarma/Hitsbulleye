"""model file for Course"""

from src.db.session import save_new_row, get_db, select_all, select_first
from src.services.logs.schema.question import QuestionLogSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class QuestionLogModel:
    """Question log model"""

    @classmethod
    def create(cls, **kw):
        """function to create question logs"""
        obj = QuestionLogSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.created_by = user_details_context.get().get("id")
        save_new_row(obj)
        return obj

    @classmethod
    def get_logs(cls, _id: int = None, question_id: int = None):
        """method to get logs by id"""
        query = db.query(QuestionLogSchema)
        if _id:
            query = query.filter(QuestionLogSchema.id == _id)
        if question_id:
            query = query.filter(QuestionLogSchema.question_id == question_id)
        if _id:
            query = select_first(query)
        else:
            if not question_id:
                query = query.limit(10)
            query = select_all(query)
        return query
