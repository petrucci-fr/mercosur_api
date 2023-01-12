from ..dplus_connection import get_data

def get_clientes(anulados: bool):

    filter = " WHERE c.anulado = 0"

    if anulados:
        filter = ""

    query = """
        SELECT c.idcliente, 
            c.nomcli, 
            c.tipoiva, 
            c.numcuit, 
            tp.descpago,
            c.diaspago,
            c.anulado
        FROM PUB.clientes c
        LEFT JOIN PUB.tipopago tp ON tp.tipopago = c.tipopago
    """ + filter

    df = get_data(query)

    return df.to_dict('records')