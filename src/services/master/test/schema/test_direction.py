"""test direction schema"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, BOOLEAN, SMALLINT, TEXT
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class TestDirectionSchema(Base):
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
