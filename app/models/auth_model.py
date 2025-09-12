from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from app import models
from app.db.base import Base
from sqlalchemy.orm import relationship, selectinload

user_supervisor_Departament = Table(
    "user_supervisor_Departament",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("User_id", Integer, ForeignKey ("users.id", ondelete="CASCADE")),
    Column("department_id", Integer, ForeignKey("departments.id", ondelete="CASCADE"))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True,index= True)
    firt_name = Column(String)
    last_name = Column(String)
    area = Column (String)
    position = Column(String)
    employee_id = Column(String)
    phone = Column(Integer)
    is_active = Column(Boolean)
    email = Column(str)
    sap_last_sync = Column(str)
    created_at = Column("createdat", DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column("updatedat", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('delivery', 'Encargado de Entrega'),
        ('audit', 'Personal de Auditoría'),
        ('employee', 'Empleado'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    area = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active_employee = models.BooleanField(default=True)
    sap_sync_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
