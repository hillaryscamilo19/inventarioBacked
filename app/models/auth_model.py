from typing import AbstractSet
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from app import models
from app.db.base import Base
from sqlalchemy.orm import relationship, selectinload

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from app.db.base import Base

user_supervisor_Departament = Table(
    "user_supervisor_Departament",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("User_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("department_id", Integer, ForeignKey("departments.id", ondelete="CASCADE"))
)

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    area = Column(String)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True, index=True)
    sap_last_sync = Column(DateTime, nullable=True)
    role = Column(String, default='employee')  # admin, delivery, audit, employee
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.role})>"

