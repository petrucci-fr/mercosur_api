from pydantic import BaseModel
from typing import Optional
import datetime


class Cliente(BaseModel):
    idcliente: int
    nomcli: str
    tipoiva: str
    numcuit: int
    descpago: str
    diaspago: int
    anulado: bool

class Comprobante(BaseModel):
    idcliente: int
    fechafac: datetime.date
    fecvence: Optional[datetime.date]
    dsdocumento: str
    origen: str
    idcomprobante: str
    descpago: str
    importe: float
    fecharec: Optional[datetime.date]
    idrecibo: Optional[str]
    imputado: float
    cancelado: bool
    vencido: bool

class Linea(BaseModel):
    codart: int
    descrip: str
    precio_unitario: float
    undsxblt: int
    bultos: int
    unidades: int
    importe_bruto: float
    bonificacion: float
    importe_neto: float
    internos: float
    iva1: float    
    importe_final: float
    precio_blt_final: float
    precio_und_final: float


class ComprobanteConLineas(Comprobante):
    lineas: list[Linea]