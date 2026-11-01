from datetime import date, datetime, timezone

from app.config import ZONA_HORARIA


def dias_de_atraso(vencimiento: date, ahora: datetime | None = None) -> int:
    """Días de atraso de una cuota impaga que vence en `vencimiento`.

    Una cuota que vence hoy todavía no está atrasada. «Hoy» es la fecha en
    Montevideo, no en UTC: a las 22:30 del 10 en Uruguay ya es 11 en UTC.
    """
    ahora = ahora or datetime.now(timezone.utc)
    hoy = ahora.astimezone(ZONA_HORARIA).date()
    return max(0, (hoy - vencimiento).days)
