import requests

from lxml import html

def response():
    params = {
        'buscadorVuelosEsb.tipoTransicion': 'S',
        'buscadorVuelosEsb.routeType': 'ONE_WAY',
        'buscadorVuelosEsb.origen': 'CUN',
        'buscadorVuelosEsb.destino': 'LIS',
        'buscadorVuelosEsb.fsalida': '20/08/2019',
        'buscadorVuelosEsb.fregreso': '23/08/2019',
        'buscadorVuelosEsb.numadultos': 1,
        'buscadorVuelosEsb.numninos': 0,
        'buscadorVuelosEsb.numbebes': 0
    }
    res = requests.post('https://en.orbest.com/b2c/pages/flight/disponibilidadSubmit.html?', params).content

    tree = html.fromstring(res)
    data = tree.xpath(
        '/html/body/div[@id="content"]'
        '/div/div/form[@id="formularioValoracion"]'
        '/div/div[@class="flexcols"]/section'
        '/div[@id="tabs2"]/div/div/ol//text()'
    )
    print(data)


response()


# {'departureAirport': 'CUN', 'arrivalAirport': 'LIS', 'depdate': '20.08.2019'}