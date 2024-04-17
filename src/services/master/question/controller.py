"""controller file for Question master"""
from src.configs.error_constant import ErrorMessage
from src.exceptions.errors.generic import EntityException
from src.services.master.question.model.area_direction import AreaDirectionModel
from src.services.master.question.model.course_model import CourseModel
from src.services.master.question.model.area_model import AreaModel
from src.services.master.question.serializer import (
    AreaInbound, AreaSingleOutbound, AreaListOutbound, AreaFinalOutbound,
    CourseInbound, CourseSingleOutbound, CourseListOutbound, CourseFinalOutbound, AreaDirectionInbound,
    AreaDirectionSingleOutbound, AreaDirectionListOutbound, AreaDirectionFinalOutbound
)
from src.utils.common import name_key_serializer


class QuestionMasterController:
    """controller class for Courses"""

    @classmethod
    async def save_course(cls, payload: CourseInbound):
        """method to save and update Course"""
        name_key = name_key_serializer(payload.name)
        course_data = CourseModel.get_by_id(name_key=name_key, status=True)
        if course_data and (not payload.id or course_data.id != payload.id):
            raise EntityException(message=ErrorMessage.RECORD_ALREADY_EXISTS)
        if payload.id:
            course_data = CourseModel.get_by_id(_id=payload.id, status=True)
            if not course_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Course"))
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        payload_dict["name_key"] = name_key
        if payload.id:
            _id = payload_dict.pop("id")
            data = CourseModel.patch(_id=_id, **payload_dict)
        else:
            data = CourseModel.create(**payload_dict)
        return await cls.get_course_by_id(_id=data.id)

    @classmethod
    async def get_course_list(cls, search_term: str = None):
        """method to get Course list"""
        name_key = name_key_serializer(search_term) if search_term else None
        data = CourseModel.get_list(name_key=name_key)
        response = []
        for each_data in data:
            response.append(CourseSingleOutbound(id=each_data.id, name=each_data.name))
        return CourseListOutbound(data=response)

    @classmethod
    async def get_course_by_id(cls, _id: int):
        """get Course by id"""
        data = CourseModel.get_by_id(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Course"))
        response = CourseSingleOutbound(id=data.id, name=data.name)
        return CourseFinalOutbound(data=response)

    @classmethod
    async def delete_course(cls, _id: int):
        """get Course by id"""
        data = CourseModel.get_by_id(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Course"))
        CourseModel.patch(_id=_id, **{"status":  False})
        return True

    @classmethod
    async def save_area(cls, payload: AreaInbound):
        """method to save and update area"""
        name_key = name_key_serializer(payload.name)
        area_data = AreaModel.get_by_id(name_key=name_key, status=True)
        if area_data and (not payload.id or area_data.id != payload.id):
            raise EntityException(message=ErrorMessage.RECORD_ALREADY_EXISTS)
        if payload.id:
            area_data = AreaModel.get_by_id(_id=payload.id, status=True)
            if not area_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        payload_dict["name_key"] = name_key
        if payload.id:
            _id = payload_dict.pop("id")
            data = AreaModel.patch(_id=_id, **payload_dict)
        else:
            data = AreaModel.create(**payload_dict)
        return await cls.get_area_by_id(_id=data.id)

    @classmethod
    async def get_area_list(cls, search_term: str = None):
        """method to get area list"""
        name_key = name_key_serializer(search_term) if search_term else None
        data = AreaModel.get_list(name_key=name_key)
        response = []
        for each_data in data:
            response.append(AreaSingleOutbound(
                id=each_data.id,
                name=each_data.name,
                area_code=each_data.area_code,
                area_type=each_data.area_type
            ))
        return AreaListOutbound(data=response)

    @classmethod
    async def get_area_by_id(cls, _id):
        """get area by id"""
        data = AreaModel.get_by_id(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        response = AreaSingleOutbound(
            id=data.id,
            name=data.name,
            area_code=data.area_code,
            area_type=data.area_type
        )
        return AreaFinalOutbound(data=response)

    @classmethod
    async def delete_area(cls, _id: int):
        """get Course by id"""
        data = AreaModel.get_by_id(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        AreaModel.patch(_id=_id, **{"status":  False})
        return True


    @classmethod
    async def save_area_direction(cls, payload: AreaDirectionInbound):
        """method to save and update area"""
        if payload.id:
            direction_data = AreaDirectionModel.get_by_id(_id=payload.id)
            if not direction_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Area Direction"))
        if payload.area_id:
            area_data = AreaModel.get_by_id(_id=payload.area_id)
            if not area_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        if payload.id:
            _id = payload_dict.pop("id")
            data = AreaDirectionModel.patch(_id=_id, **payload_dict)
        else:
            data = AreaDirectionModel.create(**payload_dict)
        return await cls.get_area_direction_by_id(_id=data.id)

    @classmethod
    async def get_area_direction_list(cls, area_id: int = None):
        """method to get area direction list"""
        data = AreaDirectionModel.get_by_id(area_id=area_id)
        response = []
        for each_data in data:
            response.append(AreaDirectionSingleOutbound(
                id=each_data.id,
                text=each_data.text,
                area_id=each_data.area_id
            ))
        return AreaDirectionListOutbound(data=response)

    @classmethod
    async def get_area_direction_by_id(cls, _id: int, area_id: int = None):
        """get area direction by id"""
        data = AreaDirectionModel.get_by_id(_id=_id, area_id=area_id)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Area Direction"))
        response = AreaDirectionSingleOutbound(
            id=data.id,
            text=data.text,
            area_id=data.area_id
        )
        return AreaDirectionFinalOutbound(data=response)

    @classmethod
    async def delete_area_direction(cls, _id: int):
        """get Course by id"""
        data = AreaDirectionModel.get_by_id(_id=_id)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Area Direction"))
        AreaDirectionModel.patch(_id=_id, **{"status":  False})
        return True

    @classmethod
    def course_get_all(cls):
        """course get all"""
        response = []
        data = CourseModel.get_list()
        for each_data in data:
            response.append(CourseSingleOutbound(id=each_data.id, name=each_data.name))
        return response

    @classmethod
    def area_get_all(cls):
        """area get all"""
        data = AreaModel.get_list()
        response = []
        for each_data in data:
            response.append(AreaSingleOutbound(
                id=each_data.id,
                name=each_data.name,
                area_code=each_data.area_code,
                area_type=each_data.area_type
            ))
        return response
