from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional
from tqdm import tqdm
from .models import Cliente, Comprobante, Linea, ComprobanteConLineas
from .dplus.queries.clientes import get_clientes
from .dplus.queries.comprobantes import get_comprobantes
from .dplus.queries.lineas import get_detalle_comprobantes


app = FastAPI(title="Mercosur DRP - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_PATH = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static"), html = True), name="static")
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@app.get("/api", response_class=HTMLResponse)
def home(request: Request):
    return TEMPLATES.TemplateResponse("index.html", {"request": request})

@app.get("/api/clientes", response_model=list[Cliente])
async def list_clientes(anulados: Optional[bool] = False):
    return get_clientes(anulados)

@app.get("/api/comprobantes/{idcliente}", response_model=list[Comprobante])
async def list_comprobantes(idcliente: int):
    return get_comprobantes(idcliente)

@app.get("/api/comprobante/{idcomprobante}", response_model=list[Linea])
async def detail_comprobante(idcomprobante: str):
    return get_detalle_comprobantes(idcomprobante)

@app.get("/api/comprobantesdet/{idcliente}", response_model=list[ComprobanteConLineas])
async def list_comprobantes_detallados(idcliente: int):
    result = []
    comprobantes = get_comprobantes(idcliente)
    for comprobante in tqdm(comprobantes):
        lineas = get_detalle_comprobantes(comprobante['idcomprobante'])
        result.append({**comprobante, "lineas": lineas})
    return result