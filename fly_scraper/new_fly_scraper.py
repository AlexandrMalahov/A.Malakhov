import datetime
import re
import requests

from lxml import html


def fly_data(way_type, dep_city, arr_city, dep_date, ret_date, *passengers):
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
    response = requests.post('https://en.orbest.com/b2c/pages/flight/disponibilidadSubmit.html?', params).content

    tree = html.fromstring(response)
    if way_type == 'ONE_WAY':

        flights = []
        data = tree.xpath(
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div/ol/li'
        )
        for info in data:
            time = info.xpath('div[@class="vuelo-wrap vuelo-wrap3"]//text()')
            flights.append(time)

        return flights

    elif way_type == 'ROUND_TRIP':

        data = tree.xpath(
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div/'
            'div[@class="wrap-sel-custom combinado"]'
            '/div[@class="grid-cols clearfix"]'
        )
        flights = []
        outbound = []
        ret_flight = []
        for info in data:
            flight = info.xpath(
                'div[@class="col2 col-first"]'
                '/div[@class="datos"]/div'
            )
            for fly in flight:
                fly_info = []
                price = fly.xpath('div[@class="precio"]//text()')
                dep_time = fly.xpath('div[@class="salida"]/span//text()')  # info.xpath wrong data
                arr_time = fly.xpath('div[@class="llegada"]/span/text()')
                fly_class = fly.xpath('div[@class="clase"]/span//text()')
                fly_way = fly.xpath('div[@class="aerop"]/span//text()')
                if len(dep_time) > 0 and len(arr_time) and len(fly_class) and len(price) > 0:
                    fly_info.append(re.findall(r'.\d+,\d{2}', price[0])[0])
                    fly_info.append(re.findall(r'\d{2}:\d{2}', dep_time[0])[0])
                    fly_info.append(re.findall(r'\d{2}:\d{2}', arr_time[0])[0])
                    fly_info.append(re.findall(r'\w+\s+\w+|\w+', fly_class[0])[0])
                    fly_info.append(' - '.join(re.findall(r'\w{3}', ' '.join(fly_way))))
                    outbound.append(fly_info)

            flight = info.xpath(
                'div[@class="col2 col-last"]'
                '/div[@class="datos"]/div'
            )

            for fly in flight:
                fly_info = []
                price = fly.xpath('div[@class="precio"]//text()')
                dep_time = fly.xpath('div[@class="salida"]/span//text()')  # info.xpath wrong data
                arr_time = fly.xpath('div[@class="llegada"]/span/text()')
                fly_class = fly.xpath('div[@class="clase"]/span/span//text()')
                fly_way = fly.xpath('div[@class="aerop"]/span//text()')
                if len(dep_time) > 0 and len(arr_time) and len(fly_class) and len(price) > 0:
                    fly_info.append(re.findall(r'.\d+,\d{2}', price[0])[0])
                    fly_info.append(re.findall(r'\d{2}:\d{2}', dep_time[0])[0])
                    fly_info.append(re.findall(r'\d{2}:\d{2}', arr_time[0])[0])
                    fly_info.append(re.findall(r'\w+\s+\w+|\w+', fly_class[0])[0])
                    fly_info.append('-'.join(re.findall(r'\w{3}', ' '.join(fly_way))))
                    ret_flight.append(fly_info)
        flights.append(outbound)
        flights.append(ret_flight)
        return flights


def correct_way():
    while True:
        way = input('Please, enter a way("ONE_WAY" or "ROUND_TRIP"): ').upper()
        if way == 'ONE_WAY' or way == 'ROUND_TRIP':
            break
        else:
            print('Incorrect flight type. Please, enter a correct way.')
    return way


def correct_dep_city():
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
    while True:
        date = input('Please, enter a departure date(dd/mm/yyyy): ')
        try:
            year = int(re.findall(r'\d{4}', date)[0])
            month = int(re.findall(r'\d{2}', date)[1])
            day = int(re.findall(r'\d{2}', date)[0])
            if datetime.date(year, month, day):
                break
        except (IndexError, ValueError):
            print('Incorrect date. Please, enter a correct date in format: day/month/year')
    return date


def correct_arr_date(func_way, func_date):
    while True:
        if func_way == 'ONE_WAY':
            date = func_date
            break
        elif way == 'ROUND_TRIP':
            date = input('Please, enter a arrival date(dd/mm/yyyy): ')
            try:
                year = int(re.findall(r'\d{4}', date)[0])
                month = int(re.findall(r'\d{2}', date)[1])
                day = int(re.findall(r'\d{2}', date)[0])
                if datetime.date(year, month, day):
                    break
            except (IndexError, ValueError):
                print('Incorrect date. Please, enter a correct date in format: day/month/year')
    return date


def correct_passengers():
    while True:
        try:
            adults = int(input('Please, enter a number of adults(number must be more than 0): '))
            if adults == 0:
                print('Incorrect number of adults.')
                continue
            children = int(input('Please, enter a number of children(number must be more or equal than 0): '))
            infants = int(input('Please, enter a number of infants(number must be more or equal than 0): '))
            if adults > 0 and children >= 0 and infants >= 0:
                break
        except ValueError:
            print('You must enter a number of passengers.')
    return adults, children, infants


if __name__ == '__main__':
    way = correct_way()
    dep_city = correct_dep_city()
    arr_city = correct_arr_city()
    dep_date = correct_dep_date()
    arr_date = correct_arr_date(way, dep_date)
    passengers = correct_passengers()
    data = fly_data(way, dep_city, arr_city, dep_date, arr_date, passengers)
    if way == 'ONE_WAY':
        for i in range(len(data)):
            print('Way:', data[i][3])
            print('Departure time:', data[i][5])
            print('Arrival time:', data[i][7])
            print('Class:', data[i][9])
            print('Price:', data[i][0])
            print('\n')
    elif way == 'ROUND_TRIP':
        print('Outbound flights', '\n')
        for info in data[0]:
            print('Way:', info[4])
            print('Departure time:', info[1])
            print('Arrival time:', info[2])
            print('Class:', info[3])
            print('Price:', info[0])
            print('\n')
        print('Return flights', '\n')
        for info in data[1]:
            print('Way:', info[4])
            print('Departure time:', info[1])
            print('Arrival time:', info[2])
            print('Class:', info[3])
            print('Price:', info[0])
            print('\n')
    if data == list():
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )
