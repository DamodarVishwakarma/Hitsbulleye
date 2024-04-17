"""file for question comment controller"""
from typing import List

from src.configs.constants import UserConstant
from src.configs.error_constant import ErrorMessage
from src.exceptions.errors.generic import EntityException
from src.services.question.model import QuestionModel
from src.services.question_comment.model import QuestionCommentModel
from src.services.question_comment.serializer import QuestionCommentInbound, QuestionCommentOutbound, \
    QuestionCommentFinalOutBound
from src.services.user.controller import user_details_context
from src.utils.common import get_user_outbound


class QuestionCommentController:
    """class for question comment thread"""

    @classmethod
    async def save(cls, payload: QuestionCommentInbound):
        """method to save comment thread"""
        if payload.id:
            data = QuestionCommentModel.get_comment_thread(_id=payload.id)
            if not data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Question Comment"))
            payload.question_id = data.question_id
            payload.parent_id = data.parent_id
        else:
            question_data = QuestionModel.get_by_id(_id=payload.question_id, status=True)
            if not question_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Question"))
            if payload.parent_id:
                parent_data = QuestionCommentModel.get_comment_thread(_id=payload.parent_id)
                if not parent_data:
                    raise EntityException(message=ErrorMessage.INVALID_ID.format("Parent"))
            else:
                payload.parent_id = 0

        payload_dict = payload.dict(exclude_unset=True, exclude_none=True)
        if "is_internal" not in payload_dict:
            payload_dict["is_internal"] = False
        if payload.id:
            _id = payload_dict.pop("id")
            save_data = QuestionCommentModel.patch(_id=_id, **payload_dict)
        else:
            save_data = QuestionCommentModel.create(**payload_dict)
        return await cls.get_comment_thread(_id=save_data.id)

    @classmethod
    async def get_comment_thread(cls, _id: int = None, parent_id: int = None, question_id: int = None):
        """method to get comment thread"""
        response = []
        data = QuestionCommentModel.get_comment_thread(_id=_id, parent_id=parent_id, question_id=question_id)
        if _id:
            if data:
                data = data.__dict__
                data["created_by"] = get_user_outbound(_id=data["created_by"])
                data["updated_by"] = get_user_outbound(_id=data["updated_by"])
                response.append(QuestionCommentOutbound(**data))
        else:
            for each_data in data or []:
                each_data = each_data.__dict__
                each_data['created_by'] = get_user_outbound(_id=each_data['created_by'])
                each_data['updated_by'] = get_user_outbound(_id=each_data['updated_by'])
                response.append(QuestionCommentOutbound(**each_data))

        return QuestionCommentFinalOutBound(data=response)

    @classmethod
    async def delete_comment_thread(cls, question_ids: List[int] = None, _ids: List[int] = None):
        """method to delete comment thread"""
        user_details = user_details_context.get()
        _ids = [_id for _id in _ids if _id] if _ids else None
        question_ids = [question_id for question_id in question_ids if question_id] if question_ids else None
        if _ids:
            for _id in _ids:
                if _id:
                    data = QuestionCommentModel.get_comment_thread(_id=_id)
                    if not data or data.created_by != user_details.get("id"):
                        _ids.remove(_id)

        if question_ids:
            if user_details.get("role_id") != UserConstant.Role.ADMIN:
                raise EntityException(message=ErrorMessage.INVALID_ACTION)
            for question_id in question_ids:
                if question_id:
                    question_data = QuestionModel.get_by_id(_id=question_id, status=True)
                    if not question_data:
                        question_ids.remove(question_id)

        QuestionCommentModel.delete_by_ids(_ids=_ids, question_ids=question_ids)
        return True
