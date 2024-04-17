"""routes for area"""
from fastapi import APIRouter, Request, Response, status
from src.services.master.question.controller import QuestionMasterController
from src.services.master.question.serializer import AreaInbound, CourseInbound, AreaDirectionInbound
from src.utils.auth import Auth

router = APIRouter()


@router.post("/area/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_area(request: Request, payload: AreaInbound):
    """route to save area"""
    return await QuestionMasterController.save_area(payload=payload)


@router.get("/area")
@Auth.authenticate_user
@Auth.authorize_user
async def get_area_list(request: Request, search_term: str = None):
    """route to get area list"""
    return await QuestionMasterController.get_area_list(search_term=search_term)


@router.get("/area/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def get_area_by_id(request: Request, id: int):
    """route to get area by id"""
    return await QuestionMasterController.get_area_by_id(_id=id)


@router.delete("/area/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_area(request: Request, id: int):
    """route to delete area"""
    await QuestionMasterController.delete_area(_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/course/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_course(request: Request, payload: CourseInbound):
    """route to save course"""
    return await QuestionMasterController.save_course(payload=payload)


@router.get("/course/")
@Auth.authenticate_user
@Auth.authorize_user
async def get_course_list(request: Request, search_term: str = None):
    """route to get course list"""
    return await QuestionMasterController.get_course_list(search_term=search_term)


@router.get("/course/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def get_course_list(request: Request, id: int):
    """route to get course by id"""
    return await QuestionMasterController.get_course_by_id(_id=id)


@router.delete("/course/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_course(request: Request, id: int):
    """route to delete course by id"""
    await QuestionMasterController.delete_course(_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/area-direction/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_area(request: Request, payload: AreaDirectionInbound):
    """route to save area"""
    return await QuestionMasterController.save_area_direction(payload=payload)


@router.get("/area-direction")
@Auth.authenticate_user
@Auth.authorize_user
async def get_area_list(request: Request, area_id: int = None):
    """route to get area list"""
    return await QuestionMasterController.get_area_direction_list(area_id=area_id)


@router.get("/area-direction/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def get_area_by_id(request: Request, id: int, area_id: int = None):
    """route to get area by id"""
    return await QuestionMasterController.get_area_direction_by_id(_id=id, area_id=area_id)


@router.delete("/area-direction/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_area(request: Request, id: int):
    """route to delete area"""
    await QuestionMasterController.delete_area_direction(_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
