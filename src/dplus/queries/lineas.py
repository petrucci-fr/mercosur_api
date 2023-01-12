from ..dplus_connection import get_data
import pandas as pd

def get_detalle_comprobantes(idcomprobante: str):

    iddocumento, letra, serie, nrodoc = str.split(idcomprobante, "-")

    iddocumento = f"'{iddocumento}'"
    letra = f"'{letra}'"

    query = f"""
        SELECT l.codart,
            a.descrip,
            l.precio AS 'precio_unitario',
            l.cant AS 'bultos',
            l.resto AS 'unidades',
            a.resto AS 'undsxblt',
            l.bonif / 100 AS 'bonificacion',
            l.internos,
            l.iva1
        FROM PUB.lineas l
        LEFT JOIN PUB.articulos a ON l.codart = a.codart
        WHERE l.anulado = 0 AND
            l.iddocumento = {iddocumento} AND
            l.letra = {letra} AND
            l.serie = {serie} AND
            l.nrodoc = {nrodoc}
    """

    df = get_data(query)

    cols = ['precio_unitario', 'bonificacion', 'internos', 'iva1']

    for col in cols:
        df[col] = df[col].apply(pd.to_numeric)

    df['blts'] =  df['bultos'] + (df['unidades'] / df['undsxblt'])
    df['importe_bruto'] = df['blts'] * df['precio_unitario']
    df['importe_neto'] = df['importe_bruto'] * (1 - df['bonificacion'])
    df['importe_final'] = df['importe_neto'] + df['internos'] + df['iva1']
    df['precio_blt_final'] = df['importe_final'] / df['blts']
    df['precio_und_final'] = df['importe_final'] / (df['blts'] * df['undsxblt'])

    df.drop(columns=['blts'], inplace=True)
    df = df[[
        'codart', 
        'descrip', 
        'precio_unitario',
        'undsxblt',
        'bultos', 
        'unidades', 
        'importe_bruto', 
        'bonificacion',
        'importe_neto',
        'internos',
        'iva1',
        'importe_final',
        'precio_blt_final',
        'precio_und_final'
    ]]

    return df.to_dict('records')