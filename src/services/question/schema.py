"""area Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, TIMESTAMP, JSONB, TEXT, BOOLEAN, SMALLINT, ARRAY
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class QuestionSchema(Base):
    """question schema"""
    __tablename__ = DBTables.QUESTION
    __table_args__ = DBConfig.BASE_ARGS

    id                    = Column(BIGINT, primary_key=True)
    org_id                = Column(BIGINT, default=0)
    is_public             = Column(BOOLEAN, default=False)
    area_ids              = Column(ARRAY(BIGINT))
    lod                   = Column(SMALLINT)
    question_style        = Column(SMALLINT)
    no_of_option          = Column(SMALLINT)  # question type objective
    marking_range         = Column(SMALLINT)  # question type subjective
    typable_text_type     = Column(SMALLINT)  # question type objective and qnaswer type typable
    direction_id          = Column(BIGINT)
    course_ids            = Column(ARRAY(BIGINT))
    question_type         = Column(SMALLINT)
    answer_type           = Column(SMALLINT)  # on save value if quetion type is objective
    editor                = Column(SMALLINT)  # onlu if question typ is subjective
    answer                = Column(ARRAY(SMALLINT))  # only if question is objective and answertype is multiple or sigle
    typable_answer        = Column(VARCHAR(250)) # question type objective and qnaswer type typable
    question              = Column(TEXT)
    explanation           = Column(TEXT)
    option1               = Column(TEXT)  # only if question is objective and answertype is multiple or sigle
    option2               = Column(TEXT)  # only if question is objective and answertype is multiple or sigle
    option3               = Column(TEXT)  # only if question is objective and answertype is multiple or sigle
    option4               = Column(TEXT)  # only if question is objective and answertype is multiple or sigle
    option5               = Column(TEXT)  # only if question is objective and answertype is multiple or sigle
    option6               = Column(TEXT)  # only if question is objective and answertype is multiple or sigle
    tags                  = Column(ARRAY(VARCHAR(200)))
    created_by            = Column(BIGINT)
    created_on            = Column(TIMESTAMP)
    updated_by            = Column(BIGINT)
    updated_on            = Column(TIMESTAMP)
    is_push_to_es         = Column(BOOLEAN, default=False)
    meta_data             = Column(JSONB, default={})
    status                = Column(BOOLEAN, default=True)
