"""area Schema file"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, TIMESTAMP, JSONB, TEXT, BOOLEAN, SMALLINT
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base


class AreaSchema(Base):
    """Course Schema"""
    __tablename__ = DBTables.AREA
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True)
    name                = Column(TEXT)
    name_key            = Column(VARCHAR(250))
    area_code           = Column(VARCHAR(250))
    area_type           = Column(SMALLINT)
    created_on          = Column(TIMESTAMP)
    created_by          = Column(BIGINT)
    updated_on          = Column(TIMESTAMP)
    updated_by          = Column(BIGINT)
    meta_data           = Column(JSONB, default={})
    status              = Column(BOOLEAN, default=True)
