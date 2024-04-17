"""routes for question comment"""
from typing import Optional
from fastapi import APIRouter, Request, Response, status
from pydantic.types import conint
from src.services.question_comment.controller import QuestionCommentController
from src.services.question_comment.serializer import QuestionCommentInbound
from src.utils.auth import Auth
from fastapi import APIRouter, Depends


router = APIRouter()



@router.post("/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_question(request: Request, payload: QuestionCommentInbound):
    """route to save user"""
    return await QuestionCommentController.save(payload=payload)


@router.delete("/delete")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_question(request: Request, question_id: int = None, _id: int = None):
    """route to delete user"""
    await QuestionCommentController.delete_comment_thread(_ids=[_id], question_ids=[question_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/get')
@Auth.authenticate_user
@Auth.authorize_user
async def get_comment_thread(
        request: Request,
        _id: Optional[conint(gt=0)] = None,
        parent_id: Optional[int] = None,
        question_id:Optional[int] = None
):
    """ route to get the question comment......"""
    return await QuestionCommentController.get_comment_thread(_id=_id, parent_id=parent_id, question_id=question_id)