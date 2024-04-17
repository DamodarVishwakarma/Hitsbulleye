"""Schema file for user auth"""

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, TIMESTAMP, SMALLINT, JSONB, ARRAY, TEXT, BOOLEAN
from src.configs.db_constants import DBTables, DBConfig
from src.db.session import Base

class UserAuthSchema(Base):
    """class User Auth model"""
    __tablename__ = DBTables.USER_AUTH
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True)
    user_id             = Column(BIGINT, nullable=True)
    name                = Column(VARCHAR(200))
    role_id             = Column(SMALLINT, default=0)
    email               = Column(VARCHAR(100), nullable=False)
    login_email         = Column(ARRAY(VARCHAR(100)))
    last_login          = Column(TIMESTAMP)
    org_id              = Column(BIGINT, default=0)
    password            = Column(VARCHAR(200), nullable=False)
    meta_data           = Column(JSONB, default=lambda: {})
    created_by          = Column(BIGINT, nullable=False)
    updated_by          = Column(BIGINT, nullable=False, default=0)
    created_on          = Column(TIMESTAMP)
    updated_on          = Column(TIMESTAMP)
    status              = Column(BOOLEAN, nullable=False, default=True)
