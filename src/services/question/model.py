"""model file for Course"""
from typing import List

from sqlalchemy_filters import apply_pagination

from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.question.schema import QuestionSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class QuestionModel:
    """User Auth model"""

    @classmethod
    def create(cls, **kw):
        """function to create user auth"""
        obj = QuestionSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        obj.created_by = user_details_context.get().get("id")
        obj.updated_by = user_details_context.get().get("id")
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method patch question data"""
        obj = (db.query(QuestionSchema).filter(QuestionSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime()
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_by_id(_id=_id)

    @classmethod
    def get_by_id(cls, _id: int = None, status: bool = None):
        """method to get area by id"""
        query = db.query(QuestionSchema)
        if _id:
            query = query.filter(QuestionSchema.id == _id)
        if status:
            query = query.filter(QuestionSchema.status == status)
        query = select_first(query)
        return query

    @classmethod
    def delete_by_ids(cls, _ids: List[int]):
        """method to delete by ids"""
        (db.query(QuestionSchema).filter(QuestionSchema.id.in_(_ids)).update(
            {
                QuestionSchema.status: False
            }
            )
        )
        db.commit()

    @classmethod
    def get(cls, page: int = 1, size: int = 50, filter: dict = {}):
        """method to get all question"""
        query = db.query(QuestionSchema)

        for key, value in filter.items() or {}:
            if key == "org_id":
                query = query.filter(QuestionSchema.org_id.in_(value))
            if key == "question_style":
                query = query.filter(QuestionSchema.question_style.in_(value))
            if key == "course_id":
                query = query.filter(QuestionSchema.course_ids.overlap(value))
            if key == "question_type":
                query = query.filter(QuestionSchema.question_type.in_(value))
            if key == "answer_type":
                query = query.filter(QuestionSchema.answer_type.in_(value))

        query = query.order_by(QuestionSchema.id.desc())
        query, pagination = apply_pagination(query, page_number=page, page_size=size)
        return select_all(query), pagination

    @classmethod
    def get_to_push_elastic(self, _id: int = None):
        """get question data"""
        query = db.query(QuestionSchema)
        if _id:
            query = query.filter(QuestionSchema.id == _id)
        else:
            query = query.filter(QuestionSchema.is_push_to_es == False)
        return select_all(query)

    @classmethod
    def update_es_status(cls, _id: int):
        """update to es status"""
        obj = (db.query(QuestionSchema).filter(QuestionSchema.id == _id).first())
        setattr(obj, "is_push_to_es", True)
        update_old_row(obj)
