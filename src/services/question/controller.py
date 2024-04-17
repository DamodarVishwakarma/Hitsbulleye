"""controller file fr question"""
from src.configs.constants import QuestionConstant
from src.configs.error_constant import ErrorMessage
from src.exceptions.errors.generic import EntityException
from src.services.master.question.model.area_model import AreaModel
from src.services.master.question.model.course_model import CourseModel
from src.services.question.model import QuestionModel
from src.services.logs.model.question import QuestionLogModel
from src.services.question.serializer import QuestionInbound, QuestionOutBound, QuestionFinalOutBound, \
    QuestionGetOutBound
from src.services.question_comment.controller import QuestionCommentController
from src.utils.common import get_user_outbound
from src.utils.common_serializer import Page


class QuestionController:
    """controller class for courses"""

    @classmethod
    async def get_all(cls, filter=None, page: int = 1, size: int = 50):
        """get all question"""
        page = page if page else 1
        size = size if size else 50
        filter = filter if filter else {}
        questions, pagination = QuestionModel.get(page=page, size=size, filter=filter)
        response_data: QuestionFinalOutBound = (QuestionFinalOutBound())
        result = []
        for data in questions or []:
            response = data.__dict__
            response["created_by"] = get_user_outbound(_id=response["created_by"])
            response["updated_by"] = get_user_outbound(_id=response["updated_by"])
            result.append(QuestionOutBound(**response))
        response_data.data = result
        page = Page()
        if pagination:
            page_number, page_size, num_pages, total_results = pagination
            page = Page(page_size=page_size, page_number=page_number, num_pages=num_pages, total_results=total_results)
        response_data.page = page
        return response_data

    @classmethod
    async def save(cls, payload: QuestionInbound):
        """method to save and update course"""
        payload_dict = payload.dict(exclude_unset=True, exclude_none=True)
        payload_dict["is_push_to_es"] = False

        if payload.question_type == QuestionConstant.QuestionType.OBJECTIVE and payload.answer_type in [
            QuestionConstant.AnswerType.SINGLE_SELECT,
            QuestionConstant.AnswerType.MULTI_SELECT] and not payload.no_of_option:
            raise EntityException(message=ErrorMessage.CUSTOM_MESSAGE.format("Please Select Number of Options"))
        if payload.no_of_option and not payload.answer:
            raise EntityException(message=ErrorMessage.CUSTOM_MESSAGE.format("Please Select Right Answer"))
        if payload.area_ids:
            for area_id in payload.area_ids:
                area_data = AreaModel.get_by_id(_id=area_id, status=True)
                if not area_data:
                    raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        if payload.course_ids:
            for course_id in payload.course_ids:
                course_data = CourseModel.get_by_id(_id=course_id, status=True)
                if not course_data:
                    raise EntityException(message=ErrorMessage.INVALID_ID.format("Course"))

        if payload.id:
            question_data = QuestionModel.get_by_id(_id=payload.id)
            if not question_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("question"))
            if payload.question:
                QuestionLogModel.create(question_id=payload.id, previous_question=question_data.question,
                                        next_question=payload.question)
            question_data = QuestionModel.patch(_id=payload.id, **payload_dict)
        else:
            question_data = QuestionModel.create(**payload_dict)

        return await cls.get_by_id(_id=question_data.id)

    @classmethod
    async def get_by_id(cls, _id: int):
        """get question by id"""
        question_data = QuestionModel.get_by_id(_id=_id, status=True)
        if not question_data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("question"))
        response = question_data.__dict__
        response["created_by"] = get_user_outbound(_id=response["created_by"])
        response["updated_by"] = get_user_outbound(_id=response["updated_by"])
        return QuestionGetOutBound(data=question_data.__dict__)

    @classmethod
    async def delete_by_ids(cls, _ids: str):
        """function to delete by ids"""
        list_ids = []
        temp_ids = _ids.split(",")
        for id in temp_ids or []:
            try:
                if int(id):
                    list_ids.append(int(id))
            except:
                pass
        list_ids = list(set(list_ids))
        if list_ids:
            QuestionModel.delete_by_ids(_ids=list_ids)
            await QuestionCommentController.delete_comment_thread(question_ids=list_ids)
        return True
