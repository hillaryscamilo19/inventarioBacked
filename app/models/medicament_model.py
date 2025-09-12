from unittest import result
from unittest.mock import Base
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

class Medicamento(Base):
    __tablename__ = "medicamento"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


def medicamento_helper(medicamento) -> dict:
    return {
        "id": medicamento.id,
        "name": medicamento.name,
    }

async def obtener_medicamento(db: AsyncSession):
    result = await db.execute(
        select(Medicamento)
        .options(
            selectinload(Medicamento.name)
        )
    )
    medicamento = result.scalars().all()
    return [medicamento_helper(c) for c in medicamento]
