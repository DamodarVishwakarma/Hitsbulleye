"""section Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, BOOLEAN, VARCHAR
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class SectionSchema(Base):
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
