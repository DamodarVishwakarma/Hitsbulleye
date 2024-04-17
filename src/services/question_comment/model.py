"""model file for question comment thred"""
from typing import List

from sqlalchemy_filters import apply_pagination

from src.db.session import save_new_row, get_db, select_first, update_old_row, select_all
from src.services.question_comment.schema import QuestionCommentSchema
from src.services.user.controller import user_details_context
from src.utils.time import get_current_datetime

db = get_db()


class QuestionCommentModel:
    """ Question Comment model """

    @classmethod
    def create(cls, **kw):
        """function to create user auth"""
        obj = QuestionCommentSchema(**kw)
        obj.created_on = get_current_datetime(return_string=False)
        obj.updated_on = get_current_datetime(return_string=False)
        obj.created_by = user_details_context.get().get("id")
        obj.updated_by = user_details_context.get().get("id")
        obj.status = True
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method patch question comment. data"""
        obj = (db.query(QuestionCommentSchema).filter(QuestionCommentSchema.id == _id).first())
        kw["updated_on"] = get_current_datetime(return_string=False)
        kw["updated_by"] = user_details_context.get().get("id")
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get_comment_thread(_id=_id)

    @classmethod
    def delete_by_ids(cls, _ids: List[int] = None, question_ids: List[int] = None):
        """method to delete by ids"""
        query = db.query(QuestionCommentSchema)
        if _ids:
            query = query.filter(QuestionCommentSchema.id.in_(_ids))
        if question_ids:
            query = query.filter(QuestionCommentSchema.question_id.in_(question_ids))

        query.update(
            {
                QuestionCommentSchema.status: False,
            }
        )
        db.commit()
        db.flush()

    @classmethod
    def get_comment_thread(cls, _id: int = None, parent_id: int = None, question_id: int = None, status: bool = True):
        """ method to get the question comment by all ids or inputs..."""
        query = db.query(QuestionCommentSchema)
        if _id:
            query = query.filter(QuestionCommentSchema.id == _id)
        if question_id:
            query = query.filter(QuestionCommentSchema.question_id == question_id)
        if parent_id:
            query = query.filter(QuestionCommentSchema.parent_id == parent_id)
        if status:
            query = query.filter(QuestionCommentSchema.status == status)
        if _id:
            query = select_first(query)
        else:
            query = select_all(query)
        return query
