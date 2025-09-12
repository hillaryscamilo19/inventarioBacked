from unittest.mock import Base
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession


class Uniforme(Base):
    __tablename__ = "Uniforme"
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False) 


def uniforme_helper(uniforme) -> dict:
    return{
        "id": uniforme.id,
        "name": uniforme.name
    }

async def obtener_uniforme(db: AsyncSession):
    result = await db.execute(
        select(Uniforme)
        .options(
            selectinload(Uniforme.id)
        )
    )

    uniforme = result.scalars().all()
    return [uniforme_helper(c) for c in uniforme]