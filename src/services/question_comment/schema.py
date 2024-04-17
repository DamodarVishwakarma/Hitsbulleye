"""Question comment Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, JSONB, TEXT, BOOLEAN
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class QuestionCommentSchema(Base):
    """question schema"""
    __tablename__ = DBTables.QUESTION_COMMENT
    __table_args__ = DBConfig.BASE_ARGS

    id                    = Column(BIGINT, primary_key=True)
    question_id           = Column(BIGINT, nullable=False)
    is_internal           = Column(BOOLEAN, default=False)
    body                  = Column(TEXT)
    parent_id             = Column(BIGINT)
    created_by            = Column(BIGINT)
    created_on            = Column(TIMESTAMP)
    updated_by            = Column(BIGINT)
    updated_on            = Column(TIMESTAMP)
    meta_data             = Column(JSONB, default={})
    status                = Column(BOOLEAN, default=True)
