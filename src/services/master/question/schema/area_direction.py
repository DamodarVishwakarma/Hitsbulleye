"""area direction Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, JSONB, TEXT, BOOLEAN
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class AreaDirectionSchema(Base):
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
