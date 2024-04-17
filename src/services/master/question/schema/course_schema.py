"""area Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, TIMESTAMP, JSONB, TEXT, BOOLEAN
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class CourseSchema(Base):
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
