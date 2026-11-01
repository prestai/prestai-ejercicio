import calendar
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

CENTAVO = Decimal("0.01")


@dataclass
class Cuota:
    numero: int
    vencimiento: date
    capital: Decimal
    interes: Decimal
    total: Decimal


def generar_cronograma(
    monto: Decimal, tea: Decimal, plazo_meses: int, primer_vencimiento: date
) -> list[Cuota]:
    """Cronograma de cuotas por sistema francés. Las reglas están en el README.

    Todo en Decimal. La cuota fija se redondea al centavo y la última cuota
    absorbe la diferencia de redondeo, para que el capital sume exacto el monto.
    """
    tasa = tasa_mensual(tea)
    cuota_fija = redondear(monto * tasa / (1 - (1 + tasa) ** -plazo_meses))
    saldo = monto
    cuotas = []
    for numero in range(1, plazo_meses + 1):
        interes = redondear(saldo * tasa)
        capital = saldo if numero == plazo_meses else cuota_fija - interes
        saldo -= capital
        vencimiento = sumar_meses(primer_vencimiento, numero - 1)
        cuotas.append(Cuota(numero, vencimiento, capital, interes, capital + interes))
    return cuotas


def tasa_mensual(tea: Decimal) -> Decimal:
    """Tasa efectiva mensual equivalente: (1 + TEA) ^ (1/12) - 1. No es TEA / 12."""
    return (1 + tea) ** (Decimal(1) / 12) - 1


def sumar_meses(fecha: date, meses: int) -> date:
    """Mismo día, `meses` después. Si ese día no existe en el mes, el último del mes."""
    indice = fecha.month - 1 + meses
    anio, mes = fecha.year + indice // 12, indice % 12 + 1
    return date(anio, mes, min(fecha.day, calendar.monthrange(anio, mes)[1]))


def redondear(valor: Decimal) -> Decimal:
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)
