from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import cliente_actual
from app.config import SCORE_MINIMO
from app.db import get_db
from app.models import Cliente
from app.schemas import ClienteOut, ElegibilidadOut
from app.servicios import obtener_score

router = APIRouter()


@router.get("/clientes", response_model=list[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    """Sólo para el selector de usuario del front (simula el login)."""
    return db.scalars(select(Cliente).order_by(Cliente.id)).all()


@router.get("/clientes/yo/elegibilidad", response_model=ElegibilidadOut)
def elegibilidad(
    cliente: Cliente = Depends(cliente_actual), db: Session = Depends(get_db)
):
    score = obtener_score(db, cliente)
    return ElegibilidadOut(elegible=score >= SCORE_MINIMO, score=score)
