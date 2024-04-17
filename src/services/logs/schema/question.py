"""area Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, TEXT
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class QuestionLogSchema(Base):
    """question schema"""
    __tablename__ = DBTables.QUESTION_LOG
    __table_args__ = DBConfig.BASE_ARGS

    id                    = Column(BIGINT, primary_key=True)
    question_id           = Column(BIGINT, default=0)
    previous_question     = Column(TEXT)
    next_question         = Column(TEXT)
    created_by            = Column(BIGINT)
    created_on            = Column(TIMESTAMP)
