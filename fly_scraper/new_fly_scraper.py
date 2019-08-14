"""Python 3.7. Parsing of the web site https://www.orbest.com/."""

import datetime
import re
import requests

from lxml import html


def fly_data(way_type, dep_city, arr_city, dep_date, ret_date, *passengers):
    """Gets connection and data from site."""

    params = {
        'buscadorVuelosEsb.tipoTransicion': 'S',
        'buscadorVuelosEsb.routeType': way_type,
        'buscadorVuelosEsb.origen': dep_city,
        'buscadorVuelosEsb.destino': arr_city,
        'buscadorVuelosEsb.fsalida': dep_date,
        'buscadorVuelosEsb.fregreso': ret_date,
        'buscadorVuelosEsb.numadultos': passengers[0][0],
        'buscadorVuelosEsb.numninos': passengers[0][1],
        'buscadorVuelosEsb.numbebes': passengers[0][2]
    }
    response = requests.post(
        'https://en.orbest.com/b2c/pages'
        '/flight/disponibilidadSubmit.html?',
        params
    ).content

    tree = html.fromstring(response)
    if way_type == 'ONE_WAY':
        flights = []  # List for lists of flights
        data = tree.xpath(
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div/ol/li'
        )
        for information in data:
            time = information.xpath(
                'div[@class="vuelo-'
                'wrap vuelo-wrap3"]//text()'
            )
            flights.append(time)

        return flights

    elif way_type == 'ROUND_TRIP':
        data = tree.xpath(  # Getting data of outbound flights
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div/'
            'div[@class="wrap-sel-custom combinado"]'
            '/div[@class="grid-cols clearfix"]'
        )
        flights = []  # List for lists of flights
        outbound = []  # Lists of outbound flights lists
        ret_flight = []  # Lists of return flights lists
        for info_1 in data:
            flight = info_1.xpath(  # Getting data of return flights
                'div[@class="col2 col-first"]'
                '/div[@class="datos"]/div'
            )
            for fly in flight:
                fly_info = []  # List of outbound flights
                price = fly.xpath('div[@class="precio"]//text()')
                dep_time = fly.xpath('div[@class="salida"]/span//text()')
                arr_time = fly.xpath('div[@class="llegada"]/span/text()')
                fly_class = fly.xpath('div[@class="clase"]/span//text()')
                fly_way = fly.xpath('div[@class="aerop"]/span//text()')
                if dep_time != [] \
                        and arr_time != [] \
                        and fly_class != [] \
                        and price != []:
                    fly_info.append(
                        re.findall(r'.\d+,\d{2}', price[0])[0]
                    )
                    fly_info.append(
                        re.findall(r'\d{2}:\d{2}', dep_time[0])[0]
                    )
                    fly_info.append(
                        re.findall(r'\d{2}:\d{2}', arr_time[0])[0]
                    )
                    fly_info.append(
                        re.findall(r'\w+\s+\w+|\w+', fly_class[0])[0]
                    )
                    fly_info.append(
                        ' - '.join(re.findall(r'\w{3}', ' '.join(fly_way)))
                    )
                    outbound.append(fly_info)

            flight = info_1.xpath(
                'div[@class="col2 col-last"]'
                '/div[@class="datos"]/div'
            )

            for fly in flight:
                fly_info = []  # List of outbound flights
                price = fly.xpath('div[@class="precio"]//text()')
                dep_time = fly.xpath('div[@class="salida"]/span//text()')
                arr_time = fly.xpath('div[@class="llegada"]/span/text()')
                fly_class = fly.xpath('div[@class="clase"]/span/span//text()')
                fly_way = fly.xpath('div[@class="aerop"]/span//text()')
                if dep_time != [] \
                        and arr_time != [] \
                        and fly_class != [] \
                        and price != []:
                    fly_info.append(re.findall(r'.\d+,\d{2}', price[0])[0])
                    fly_info.append(re.findall(r'\d{2}:\d{2}', dep_time[0])[0])
                    fly_info.append(re.findall(r'\d{2}:\d{2}', arr_time[0])[0])
                    fly_info.append(
                        re.findall(r'\w+\s+\w+|\w+', fly_class[0])[0]
                    )
                    fly_info.append(
                        '-'.join(re.findall(r'\w{3}', ' '.join(fly_way)))
                    )
                    ret_flight.append(fly_info)
        flights.append(outbound)
        flights.append(ret_flight)
        return flights


def correct_way():
    """Checking and input a flight type."""

    while True:
        way = input('Please, enter a way("ONE_WAY" or "ROUND_TRIP"): ').upper()
        if way == 'ONE_WAY' or way == 'ROUND_TRIP':
            break
        else:
            print('Incorrect flight type. Please, enter a correct way.')
    return way


def correct_dep_city():
    """Checking and input IATA code of departure airport."""

    iata = ['CUN', 'LIS', 'PUJ']
    while True:
        city = input('Please, enter IATA code departure city: ').upper()
        if city in iata:
            break
        else:
            print(
                'Incorrect iata code. Please, '
                'enter a correct iata code("{}" '
                'or "{}" or "{}")'.format(
                    iata[0], iata[1], iata[2]
                )
            )
    return city


def correct_arr_city():
    """Checking and input IATA code of arrival airport."""

    iata = ['CUN', 'LIS', 'PUJ']
    while True:
        city = input('Please, enter IATA code arrival city: ').upper()
        if city in iata:
            break
        else:
            print(
                'Incorrect iata code. Please, '
                'enter a correct iata code("{}" '
                'or "{}" or "{}")'.format(
                    iata[0], iata[1], iata[2]
                )
            )
    return city


def correct_dep_date():
    """Input and checking for correctness departure date."""

    while True:
        date = input('Please, enter a departure date(dd/mm/yyyy): ')
        try:
            year = int(re.findall(r'\d{4}', date)[0])
            month = int(re.findall(r'\d{2}', date)[1])
            day = int(re.findall(r'\d{2}', date)[0])
            if datetime.date(year, month, day):
                break
        except (IndexError, ValueError):
            print(
                'Incorrect date. Please, enter a '
                'correct date in format: day/month/year'
            )
    return date


def correct_arr_date(func_way, func_date):
    """Input and checking for correctness return date."""

    while True:
        if func_way == 'ONE_WAY':
            date = func_date
            break
        elif func_way == 'ROUND_TRIP':
            date = input('Please, enter a arrival date(dd/mm/yyyy): ')
            try:
                year = int(re.findall(r'\d{4}', date)[0])
                month = int(re.findall(r'\d{2}', date)[1])
                day = int(re.findall(r'\d{2}', date)[0])
                if datetime.date(year, month, day):
                    break
            except (IndexError, ValueError):
                print(
                    'Incorrect date. Please, enter a '
                    'correct date in format: day/month/year'
                )
    return date


def correct_passengers():
    """Checking and input number of passengers."""

    while True:
        try:
            adults = int(
                input(
                    'Please, enter a number of adults'
                    '(number must be more than 0): '
                )
            )
            if adults <= 0:
                print('Incorrect number of adults.')
                continue
            children = int(
                input(
                    'Please, enter a number of children'
                    '(number must be more or equal than 0): '
                )
            )
            if children < 0:
                print('Incorrect number of children.')
                continue
            infants = int(
                input(
                    'Please, enter a number of infants'
                    '(number must be more or equal than 0): '
                )
            )
            if infants < 0:
                print('Incorrect number of infants.')
                continue
            return adults, children, infants
        except ValueError:
            print('Number of passengers must be integer number.')


if __name__ == '__main__':
    TYPE_WAY = correct_way()
    DEPARTURE_CITY = correct_dep_city()
    ARRIVAL_CITY = correct_arr_city()
    DEPARTURE_DATE = correct_dep_date()
    RETURN_DATE = correct_arr_date(TYPE_WAY, DEPARTURE_DATE)
    PASSENGERS_NUM = correct_passengers()
    DATA_FLIGHTS = fly_data(
        TYPE_WAY,
        DEPARTURE_CITY,
        ARRIVAL_CITY,
        DEPARTURE_DATE,
        RETURN_DATE,
        PASSENGERS_NUM
    )
    if DATA_FLIGHTS == list() or DATA_FLIGHTS == [[], []]:
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )
    else:
        if TYPE_WAY == 'ONE_WAY':
            for i in range(len(DATA_FLIGHTS)):
                print('Way:', DATA_FLIGHTS[i][3])
                print('Departure time:', DATA_FLIGHTS[i][5])
                print('Arrival time:', DATA_FLIGHTS[i][7])
                print('Class:', DATA_FLIGHTS[i][9])
                print('Price:', DATA_FLIGHTS[i][0])
                print('\n')
        elif TYPE_WAY == 'ROUND_TRIP':
            print('Outbound flights', '\n')
            for info in DATA_FLIGHTS[0]:
                print('Way:', info[4])
                print('Departure time:', info[1])
                print('Arrival time:', info[2])
                print('Class:', info[3])
                print('Price:', info[0])
                print('\n')
            print('Return flights', '\n')
            for inform in DATA_FLIGHTS[1]:
                print('Way:', inform[4])
                print('Departure time:', inform[1])
                print('Arrival time:', inform[2])
                print('Class:', inform[3])
                print('Price:', inform[0])
                print('\n')
