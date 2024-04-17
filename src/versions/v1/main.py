"""
main
"""
from fastapi import APIRouter
from src.versions.v1.routes import master_question, user, lookup, question, question_comment, master_test

api_router = APIRouter()

api_router.include_router(master_question.router, prefix="/v1/master/question", tags=["Master Question"])
api_router.include_router(master_test.router, prefix="/v1/master/test", tags=["Master Test"])
api_router.include_router(question.router, prefix="/v1/question", tags=["Question"])
api_router.include_router(question_comment.router, prefix="/v1/question-comment", tags=["Question Comment"])
api_router.include_router(user.router, prefix="/v1/user", tags=["User"])
api_router.include_router(lookup.router, prefix="/v1/lookup", tags=["Lookup"])
