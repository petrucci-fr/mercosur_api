from ..dplus_connection import get_data
import pandas as pd
import numpy as np
from datetime import datetime

def get_comprobantes(idcliente: int):

    query = f"""
        SELECT m.idcliente,
            m.fechafac,
            m.fecvence,
            td.dsdocumento,
            m.origen,
            m.iddocumento + '-' + m.letra + '-' + CONVERT('VARCHAR', m.serie) + '-' + CONVERT('VARCHAR', m.nrodoc) AS 'idcomprobante',
            tp.descpago,
            CASE
                WHEN m.iddocumento IN ('DVVTA', 'PRDVO') THEN -1 * (m.netogra + m.internos + m.iva1)
                ELSE m.netogra + m.internos + m.iva1
            END AS 'importe',
            mr.fecharec,
            CONVERT('VARCHAR', lr.serierec) + '-' + CONVERT('VARCHAR', lr.nrorecibo) AS 'idrecibo',
            CASE 
                WHEN lr.entrega IS NULL THEN 0
                WHEN m.iddocumento IN ('DVVTA', 'PRDVO') THEN -1 * lr.entrega
                ELSE lr.entrega
            END AS 'imputado'
        FROM PUB.mascara m
        LEFT JOIN PUB.tipodocs td ON m.iddocumento = td.iddocumento
        LEFT JOIN PUB.tipopago tp ON m.ctacte = tp.tipopago
        LEFT JOIN PUB.linrec lr ON
            m.iddocumento = lr.iddocumento AND
            m.letra = lr.letra AND 
            m.serie = lr.serie AND 
            m.nrodoc = lr.nrodoc
        LEFT JOIN PUB.mascrec mr ON 
            lr.serierec = mr.serierec AND 
            lr.nrorecibo = mr.nrorecibo
            /* TODO: Quitar Presupuestos del filtro de iddocumento */
        WHERE m.iddocumento IN ('FCVTA', 'DVVTA') AND 
            m.fechafac >= TIMESTAMPADD(SQL_TSI_DAY, -90, CURDATE()) AND 
            m.idcliente = {idcliente}
        ORDER BY m.fechafac, m.nrodoc DESC
    """

    df = get_data(query)

    
    df['cancelado'] = np.where(df['imputado'] == df['importe'], True, False)
    df['vencido'] = np.where(pd.to_datetime(df['fecvence']) < datetime.today().strftime('%Y-%m-%d'), True, False)

    return df.to_dict('records')