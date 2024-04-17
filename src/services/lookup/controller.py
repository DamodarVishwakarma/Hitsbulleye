"""controller file for lookup controller"""
from src.configs.lookup_constant import QUESTION
from src.services.lookup.serializer import LookupOutBound, Model
from src.services.master.question.controller import QuestionMasterController
from src.utils.common_serializer import SuccessResponsePartial


class LookupController:
    """lookup controller class"""

    @classmethod
    async def get_lookup_data(cls, models):
        """get lookup data"""
        lookup_out_bound: LookupOutBound = LookupOutBound()
        for model in models:
            if Model.QUESTION == model:
                lookup_out_bound.question = QUESTION
            elif Model.COURSE == model:
                lookup_out_bound.course = QuestionMasterController.course_get_all()
            elif Model.AREA == model:
                lookup_out_bound.area = QuestionMasterController.area_get_all()

        return SuccessResponsePartial(data=lookup_out_bound)
