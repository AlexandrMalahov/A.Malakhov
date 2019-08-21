"""Python 3.7. Parsing of the web site https://www.orbest.com/."""
# сделать с аргпарс и объеденить проверки ввода в одну функцию


import datetime
import re
import requests
import sys

from lxml import html


def connection(way_type, dep_city, arr_city, dep_date, ret_date, passengers):
    """Function gets params of searching and set connection with site."""

    params = {
        'buscadorVuelosEsb.tipoTransicion': 'S',
        'buscadorVuelosEsb.routeType': way_type,
        'buscadorVuelosEsb.origen': dep_city,
        'buscadorVuelosEsb.destino': arr_city,
        'buscadorVuelosEsb.fsalida': dep_date,
        'buscadorVuelosEsb.fregreso': ret_date,
        'buscadorVuelosEsb.numadultos': passengers[0],
        'buscadorVuelosEsb.numninos': passengers[1],
        'buscadorVuelosEsb.numbebes': passengers[2]
    }
    tree = html.fromstring(
        requests.post(
            'https://en.orbest.com/b2c'
            '/pages/flight/disponibili'
            'dadSubmit.html?', params
        ).content
    )
    return tree


def fly_data(way_type, connect_func):
    """Gets data from site."""

    tree = connect_func
    flights = [[], []]  # List of vars of flights
    # (first lis for outbound flights, second list for return flight)
    if way_type == 'ONE_WAY':
        data = tree.xpath(
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div/ol/li'
        )
        flights = [  # List of lists of flights
            information.xpath(
                'div[@class="vuelo-wrap'
                ' vuelo-wrap3"]//text()'
            ) for information in data
        ]

    elif way_type == 'ROUND_TRIP':
        data = tree.xpath(               # Getting data of outbound flights
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div/'
            'div[@class="wrap-sel-custom combinado"]'
            '/div[@class="grid-cols clearfix"]'
        )

        for details in data:
            flight_first = ' '.join(
                details.xpath(
                    'div[@class="col2 col-first"]'
                    '/div[@class="datos"]/div//text()'
                )
            )  # Getting data of departure flights

            fly_class = details.xpath(
                'div[@class="col2 col-first"]'
                '/div[@class="datos"]/div'
                '/div[@class="clase"]/span//text()'
            )
            cities = re.findall(r'\b\w{3}\b', flight_first)
            time = re.findall(r'\d{1,2}:\d{2}', flight_first)
            price = re.findall(r'.\d+,\d{2}', flight_first)
            time = [time[i:i+2] for i in range(0, len(time), 2)]

            for i, class_type in enumerate(fly_class):
                flights[0].append(
                    [cities[0],
                     cities[1],
                     class_type,
                     price[i],
                     time[i][0],
                     time[i][1]]
                )

            flight_last = ' '.join(details.xpath(
                'div[@class="col2 col-last"]'
                '/div[@class="datos"]/div//text()'
            ))  # Getting data of return flights

            fly_class = details.xpath(
                'div[@class="col2 col-last"]'
                '/div[@class="datos"]/div'
                '/div[@class="clase"]/span//text()'
            )
            cities = re.findall(r'\b\w{3}\b', flight_last)
            time = re.findall(r'\d{1,2}:\d{2}', flight_last)
            price = re.findall(r'.\d+,\d{2}', flight_last)
            time = [time[i:i+2] for i in range(0, len(time), 2)]

            for i, class_type in enumerate(fly_class):
                flights[1].append([
                    cities[0],
                    cities[1],
                    class_type,
                    price[i],
                    time[i][0],
                    time[i][1]
                ])

    return flights


def correct_way(count):
    """Checking and input a flight type."""

    try:
        if count != 0:
            raise IndexError
        way = sys.argv[1].upper()
        if way == 'ONE_WAY' or way == 'ROUND_TRIP':
            return way
        else:
            raise IndexError
    except IndexError:
        while True:
            way = input(
                'Please, enter a way'
                '("ONE_WAY" or "ROUND_TRIP"): '
            ).upper()
            if way == 'ONE_WAY' or way == 'ROUND_TRIP':
                break
            else:
                print('Incorrect flight type. Please, enter a correct way.')
        return way


def correct_dep_city(count):
    """Checking and input IATA code of departure airport."""

    iata_code = ['CUN', 'LIS', 'PUJ']
    try:
        if count != 0:
            raise IndexError
        city = sys.argv[2].upper()
        if city in iata_code:
            return city
        else:
            raise IndexError
    except IndexError:
        while True:
            city = input('Please, enter IATA code departure city: ').upper()
            if city in iata_code:
                break
            else:
                print(
                    'Incorrect iata code. Please, '
                    'enter a correct iata code("{}" '
                    'or "{}" or "{}")'.format(
                        iata_code[0], iata_code[1], iata_code[2]
                    )
                )
        return city


def correct_arr_city(count):
    """Checking and input IATA code of arrival airport."""

    iata_code = ['CUN', 'LIS', 'PUJ']

    try:
        if count != 0:
            raise IndexError
        city = sys.argv[3].upper()
        if city in iata_code:
            return city
        else:
            raise IndexError
    except IndexError:
        while True:
            city = input('Please, enter IATA code arrival city: ').upper()
            if city in iata_code:
                break
            else:
                print(
                    'Incorrect iata code. Please, '
                    'enter a correct iata code("{}" '
                    'or "{}" or "{}")'.format(
                        iata_code[0], iata_code[1], iata_code[2]
                    )
                )
        return city


def correct_dep_date(count):
    """Input and checking for correctness departure date."""

    try:
        if count != 0:
            raise IndexError
        date = sys.argv[4]
        date = re.findall(r'(\d|\d{2}).(\d|\d{2}).(\d{4})', date)[0]
        if datetime.date(int(date[2]), int(date[1]), int(date[0])):
            pass

    except (IndexError, ValueError):
        while True:
            date = input('Please, enter a departure date(dd/mm/yyyy): ')
            try:
                date = re.findall(r'(\d|\d{2}).(\d|\d{2}).(\d{4})', date)[0]
                if datetime.date(int(date[2]), int(date[1]), int(date[0])):
                    break
            except (IndexError, ValueError):
                print(
                    'Incorrect date. Please, enter a '
                    'correct date in format: day/month/year'
                )

    return '/'.join(date)


def correct_ret_date(func_way, func_date, count):
    """Input and checking for correctness return date."""

    while True:
        if func_way == 'ONE_WAY':
            date = func_date
            return date
        elif func_way == 'ROUND_TRIP':
            try:
                if count != 0:
                    raise IndexError
                date = sys.argv[5]
                date = re.findall(r'(\d|\d{2}).(\d|\d{2}).(\d{4})', date)[0]
                if datetime.date(int(date[2]), int(date[1]), int(date[0])):
                    return '/'.join(date)
            except (IndexError, ValueError):
                date = input('Please, enter a return date(dd/mm/yyyy): ')
                try:
                    date = re.findall(
                        r'(\d|\d{2}).(\d|\d{2}).(\d{4})',
                        date
                    )[0]
                    if datetime.date(int(date[2]), int(date[1]), int(date[0])):
                        return '/'.join(date)
                except (IndexError, ValueError):
                    print(
                        'Incorrect date. Please, enter a '
                        'correct date in format: day/month/year'
                    )


def correct_passengers(way_func, count):
    """Checking and input number of passengers."""

    try:
        if count != 0:
            raise IndexError
        if way_func == 'ONE_WAY':
            adults = int(sys.argv[5])
            children = int(sys.argv[6])
            infants = int(sys.argv[7])
        elif way_func == 'ROUND_TRIP':
            adults = int(sys.argv[6])
            children = int(sys.argv[7])
            infants = int(sys.argv[8])
        else:
            raise ValueError
        if adults <= 0 or children < 0 or infants < 0:
            raise ValueError
        return adults, children, infants
    except (IndexError, ValueError):
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
                continue


def data_print(data_func):
    """Result printing."""

    if data_func == list() or data_func == [[], []]:
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )
    else:
        if type_way == 'ONE_WAY':
            for i, _ in enumerate(data_func):
                print('Way:', data_func[i][3])
                print('Departure time:', data_func[i][5])
                print('Arrival time:', data_func[i][7])
                print('Class:', data_func[i][9])
                print('Price:', data_func[i][0])
                print('\n')
        elif type_way == 'ROUND_TRIP':
            print('Outbound flights', '\n')
            for info in data_func[0]:
                print('Way: {0}-{1}'.format(info[0], info[1]))
                print('Departure time:', info[4])
                print('Arrival time:', info[5])
                print('Class:', info[2])
                print('Price:', info[3])
                print('\n')
            print('Return flights', '\n')
            for inform in data_func[1]:
                print('Way: {0}-{1}'.format(inform[0], inform[1]))
                print('Departure time:', inform[4])
                print('Arrival time:', inform[5])
                print('Class:', inform[2])
                print('Price:', inform[3])
                print('\n')


if __name__ == '__main__':
    query = input_query_params()
    query = query if query or manual_input()
    counter = 0  # counter of program calls
    # (for usability program in command line)
    while True:
        type_way = correct_way(counter)
        departure_city = correct_dep_city(counter)
        arrival_city = correct_arr_city(counter)
        departure_date = correct_dep_date(counter)
        return_date = correct_ret_date(type_way, departure_date, counter)
        passengers_num = correct_passengers(type_way, counter)

        connect = connection(
            type_way,
            departure_city,
            arrival_city,
            departure_date,
            return_date,
            passengers_num
        )
        data_flights = fly_data(type_way, connect)
        data_print(data_flights)
        escape = input('For exit enter "q". For continue enter any key.')
        print('\n')
        if escape == 'q':
            break
        else:
            counter += 1
