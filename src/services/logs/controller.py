"""controller file fr question"""
from src.services.logs.model.question import QuestionLogModel
from src.services.logs.serializer import LogsOutBound, LogsGetOutBound
from src.utils.common import get_user_outbound


class LogsController:
    """controller class for question log"""

    @classmethod
    async def get_question_logs(cls, _id: int = None, question_id: int = None):
        """get question log by id"""
        question_data = QuestionLogModel.get_logs(_id=_id, question_id=question_id)
        response = []
        if _id and question_data:
            data = question_data.__dict__
            data["created_by"] = get_user_outbound(_id=data["created_by"])
            response.append(LogsOutBound(**data))
        else:
            for data in question_data or []:
                data = data.__dict__
                data["created_by"] = get_user_outbound(_id=data["created_by"])
                response.append(LogsOutBound(**data))
        return LogsGetOutBound(data=response)
