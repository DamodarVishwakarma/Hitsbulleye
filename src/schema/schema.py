"""Definition of all model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    BOOLEAN,
    SMALLINT,
    VARCHAR,
    TIMESTAMP, JSONB, ARRAY, TEXT
)

from src.configs.db_constants import DBConfig, DBTables

Base = declarative_base()


class UserAuthModel(Base):
    """class User Auth model"""
    __tablename__ = DBTables.USER_AUTH
    __table_args__ = DBConfig.BASE_ARGS

    id                       = Column(BIGINT, primary_key=True)
    user_id                  = Column(BIGINT, nullable=True)
    name                     = Column(VARCHAR(200))
    role_id                  = Column(SMALLINT, default=0)
    email                    = Column(VARCHAR(100), nullable=False)
    login_email              = Column(ARRAY(VARCHAR(100)))
    last_login               = Column(TIMESTAMP)
    org_id                   = Column(BIGINT, default=0)
    password                 = Column(VARCHAR(200), nullable=False)
    meta_data                = Column(JSONB, default=lambda: {})
    created_by               = Column(BIGINT, nullable=False)
    updated_by               = Column(BIGINT, nullable=False, default=0)
    created_on               = Column(TIMESTAMP)
    updated_on               = Column(TIMESTAMP)
    status                   = Column(BOOLEAN, nullable=False, default=True)


class QuestionModel(Base):
    """question schema"""
    __tablename__ = DBTables.QUESTION
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True)
    org_id              = Column(BIGINT, default=0)
    is_public           = Column(BOOLEAN, default=False)
    area_ids            = Column(ARRAY(BIGINT))
    lod                 = Column(SMALLINT)
    question_style      = Column(SMALLINT)
    no_of_option        = Column(SMALLINT)   # question type objective
    marking_range       = Column(SMALLINT)  # question type subjective
    typable_text_type   = Column(SMALLINT)  # question type objective and qnaswer type typable
    direction_id        =  Column(BIGINT)
    course_ids          = Column(ARRAY(BIGINT))
    question_type       = Column(SMALLINT)
    answer_type         = Column(SMALLINT)   # on save value if quetion type is objective
    editor              = Column(SMALLINT)   # onlu if question typ is subjective
    answer              = Column(ARRAY(SMALLINT))  # only if question is objective and answertype is multiple or sigle
    typable_answer      = Column(VARCHAR(250))  # question type objective and qnaswer type typable
    question            = Column(TEXT)
    explanation         = Column(TEXT)
    option1             = Column(TEXT)          # only if question is objective and answertype is multiple or sigle
    option2             = Column(TEXT)          # only if question is objective and answertype is multiple or sigle
    option3             = Column(TEXT)          # only if question is objective and answertype is multiple or sigle
    option4             = Column(TEXT)          # only if question is objective and answertype is multiple or sigle
    option5             = Column(TEXT)          # only if question is objective and answertype is multiple or sigle
    option6             = Column(TEXT)          # only if question is objective and answertype is multiple or sigle
    tags                = Column(ARRAY(VARCHAR(200)))
    created_on          = Column(TIMESTAMP)
    created_by          = Column(BIGINT)
    updated_on          = Column(TIMESTAMP)
    updated_by          = Column(BIGINT)
    is_push_to_es       = Column(BOOLEAN, default=False)
    meta_data           = Column(JSONB, default={})
    status              = Column(BOOLEAN, default=True)


class AreaModel(Base):
    """Course Schema"""
    __tablename__ = DBTables.AREA
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True)
    name                = Column(TEXT)
    area_code           = Column(VARCHAR(250))
    area_type           = Column(SMALLINT)
    name_key            = Column(VARCHAR(250))
    created_on          = Column(TIMESTAMP)
    created_by          = Column(BIGINT)
    updated_on          = Column(TIMESTAMP)
    updated_by          = Column(BIGINT)
    meta_data           = Column(JSONB, default={})
    status              = Column(BOOLEAN, default=True)


class CourseModel(Base):
    """Course Schema"""
    __tablename__ = DBTables.COURSE
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True)
    name                = Column(TEXT)
    name_key            = Column(VARCHAR(250))
    created_on          = Column(TIMESTAMP)
    created_by          = Column(BIGINT)
    updated_on          = Column(TIMESTAMP)
    updated_by          = Column(BIGINT)
    meta_data           = Column(JSONB, default={})
    status              = Column(BOOLEAN, default=True)


class AreaDirectionModel(Base):
    """Area Direction"""

    __tablename__ = DBTables.AREA_DIRECTION
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True)
    area_id             = Column(BIGINT)
    text                = Column(TEXT)
    created_on          = Column(TIMESTAMP)
    created_by          = Column(BIGINT)
    updated_on          = Column(TIMESTAMP)
    updated_by          = Column(BIGINT)
    meta_data           = Column(JSONB, default={})
    status              = Column(BOOLEAN, default=True)


class QuestionCommentModel(Base):
    """question schema"""

    __tablename__ = DBTables.QUESTION_COMMENT
    __table_args__ = DBConfig.BASE_ARGS

    id                    = Column(BIGINT, primary_key=True)
    question_id           = Column(BIGINT,nullable=False)
    is_internal           = Column(BOOLEAN,default=False)
    body                  = Column(TEXT)
    parent_id             = Column(BIGINT)
    created_by            = Column(BIGINT)
    created_on            = Column(TIMESTAMP)
    updated_by            = Column(BIGINT)
    updated_on            = Column(TIMESTAMP)
    meta_data             = Column(JSONB, default={})
    status                = Column(BOOLEAN, default=True)


class SectionModel(Base):
    """class for test section"""

    __tablename__ = DBTables.TEST_SECTION
    __table_args__ = DBConfig.BASE_ARGS

    id          = Column(BIGINT, primary_key=True)
    name        = Column(VARCHAR(250))
    name_key    = Column(VARCHAR(250))
    created_by  = Column(BIGINT)
    created_on  = Column(TIMESTAMP)
    updated_by  = Column(BIGINT)
    updated_on  = Column(TIMESTAMP)
    status      = Column(BOOLEAN, default=True)


class TestDirectionModel(Base):
    """class for test section"""

    __tablename__ = DBTables.TEST_DIRECTION
    __table_args__ = DBConfig.BASE_ARGS

    id          = Column(BIGINT, primary_key=True)
    domain_id   = Column(SMALLINT)
    test_type   = Column(SMALLINT)
    direction   = Column(TEXT)
    created_by  = Column(BIGINT)
    created_on  = Column(TIMESTAMP)
    updated_by  = Column(BIGINT)
    updated_on  = Column(TIMESTAMP)
    status      = Column(BOOLEAN, default=True)


class TestExplanationModel(Base):
    """class for test section"""

    __tablename__ = DBTables.TEST_EXPLANATION
    __table_args__ = DBConfig.BASE_ARGS

    id          = Column(BIGINT, primary_key=True)
    test_type   = Column(SMALLINT)
    explanation = Column(TEXT)
    created_by  = Column(BIGINT)
    created_on  = Column(TIMESTAMP)
    updated_by  = Column(BIGINT)
    updated_on  = Column(TIMESTAMP)
    status      = Column(BOOLEAN, default=True)

class QuestionLogModel(Base):
    """question schema"""
    __tablename__ = DBTables.QUESTION_LOG
    __table_args__ = DBConfig.BASE_ARGS

    id                    = Column(BIGINT, primary_key=True)
    question_id           = Column(BIGINT, default=0)
    previous_question     = Column(TEXT)
    next_question         = Column(TEXT)
    created_by            = Column(BIGINT)
    created_on            = Column(TIMESTAMP)

Index("user_auth_user_login_email_key_", UserAuthModel.login_email, unique=False)
Index("user_auth_email_key_", UserAuthModel.email, unique=False)
Index("area_name_key_", AreaModel.name_key, unique=False)
Index("course_name_key_", CourseModel.name_key, unique=False)
Index("area_direction_area_id_key_", AreaDirectionModel.area_id, unique=False)
Index("question_comment_question_id_key_", QuestionCommentModel.question_id, unique=False)
Index("question_logs_question_id_key_", QuestionLogModel.question_id, unique=False)
