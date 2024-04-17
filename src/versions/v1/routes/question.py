"""routes for question"""
from typing import Optional
from fastapi import APIRouter, Request, Response, status
from pydantic.types import conint
from src.services.question.controller import QuestionController
from src.services.logs.controller import LogsController
from src.services.question.serializer import QuestionInbound, GetAllQuestionInbound
from src.utils.auth import Auth
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends
from src.db.session import ES_HOST
from src.services.elastic_search.controller import ElasticSearchController

router = APIRouter()


def get_elasticsearch() -> Elasticsearch:
    """Get elastic search"""
    e_s = Elasticsearch(hosts=[ES_HOST], timeout=30)
    return e_s


@router.post("/all")
@Auth.authenticate_user
@Auth.authorize_user
async def get_all(request: Request, payload: Optional[GetAllQuestionInbound]):
    """route to save user"""
    payload = GetAllQuestionInbound(**payload.dict(exclude_unset=True, exclude_none=True))
    filter = payload.filter.dict(exclude_unset=True, exclude_none=True) if payload.filter else {}
    return await QuestionController.get_all(page=payload.page, filter=filter, size=payload.size)


@router.post("/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_question(request: Request, payload: QuestionInbound):
    """route to save user"""
    return await QuestionController.save(payload=payload)


@router.get("/get")
@Auth.authenticate_user
@Auth.authorize_user
async def get(request: Request, _id: conint(gt=0)):
    """route to save user"""
    return await QuestionController.get_by_id(_id=_id)


@router.delete("/delete")
@Auth.authenticate_user
@Auth.authorize_user
async def delete(request: Request, _ids: str):
    """route to save user"""
    await QuestionController.delete_by_ids(_ids=_ids)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/search/company")
@Auth.authenticate_user
@Auth.authorize_user
async def filter(
        request: Request,
        es: Elasticsearch = Depends(get_elasticsearch),
        payload: dict = {},
        page: int = 1,
        size: int = 50
):
    """search question"""
    return ElasticSearchController(es).filters(payload=payload, page=page, size=size)


# /logs
# new route get logs
# query params -- id, quetsion id:
# then call controller logs conteroller.get_question_logs

@router.get("/logs")
@Auth.authenticate_user
@Auth.authorize_user
async def get(request: Request, _id: Optional[conint(gt=0)] = None, question_id: Optional[conint(gt=0)] = None):
    """route to save question logs"""
    return await LogsController.get_question_logs(_id=_id, question_id=question_id)
