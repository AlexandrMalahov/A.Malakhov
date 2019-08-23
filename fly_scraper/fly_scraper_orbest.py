"""Python 3.7. Parsing of the web site https://www.orbest.com/."""


import argparse
import datetime
import re
import requests

from lxml import html


def input_query_params():
    """Parsing arguments of command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-w', '--way',
        help='input way type'
             '("ONE_WAY" or "ROUND_TRIP")'
    )
    parser.add_argument(
        '-d', '--dep_city',
        help='input departure city'
             '("LIS", "CUN", "PUJ")'
    )
    parser.add_argument(
        '-a', '--arr_city',
        help='input arrival city'
             '("LIS", "CUN", "PUJ")'
    )
    parser.add_argument('-d_d', '--dep_date', help='input a departure date')
    parser.add_argument('-r', '--ret_date', help='input a return date')
    parser.add_argument(
        '-n_a', '--num_adults',
        help='input a number of adults'
    )
    parser.add_argument(
        '-n_c', '--num_child',
        help='input a number of children'
    )
    parser.add_argument(
        '-n_i', '--num_infants',
        help='input a number of infants'
    )
    args = parser.parse_args()
    params = (
        args.way, args.dep_city,
        args.arr_city, args.dep_date,
        args.ret_date, args.num_adults,
        args.num_child, args.num_infants
    )
    return params


def manual_input(count=0):
    """User input validation."""

    if count == 0:
        query_params = input_query_params()
        way = query_params[0]
        dep_city = query_params[1]
        arr_city = query_params[2]
        dep_date = query_params[3]
        ret_date = query_params[4]
        adults = query_params[5]
        children = query_params[6]
        infants = query_params[7]
    else:
        way = input(
            'Please, enter a way'
            '("ONE_WAY" or "ROUND_TRIP"): '
        )
        dep_city = input('Please, enter IATA code of departure city: ')
        arr_city = input('Please, enter IATA code of arrival city: ')
        dep_date = input('Please, enter a departure date(dd/mm/yyyy): ')
        ret_date = dep_date
        if way.upper() == 'ROUND_TRIP':
            ret_date = input('Please, enter a return date(dd/mm/yyyy): ')
        adults = input(
            'Please, enter a number of adults'
            '(number must be more than 0 and less or equal 9): '
        )
        children = input(
            'Please, enter a number of children'
            '(number must be more or equal than '
            '0 and less or equal number of adults): '
        )
        infants = input(
            'Please, enter a number of infants'
            '(number must be more or equal than '
            '0 and less or equal number of adults): '
        )

    while True:  # Checking and input a flight type.
        if way is None:
            way = input(
                'Please, enter a way'
                '("ONE_WAY" or "ROUND_TRIP"): '
            ).upper()
        else:
            way = way.upper()
        if way == 'ONE_WAY' or way == 'ROUND_TRIP':
            break
        else:
            print('Incorrect flight type. Please, enter a correct way.')
            way = input(
                'Please, enter a way'
                '("ONE_WAY" or "ROUND_TRIP"): '
            )

    iata_code = ['CUN', 'LIS', 'PUJ']
    # Checking and input IATA code of departure airport

    while True:
        if dep_city is None:
            dep_city = input(
                'Please, enter IATA '
                'code of departure city: '
            ).upper()
        else:
            dep_city = dep_city.upper()
        if dep_city in iata_code:
            break
        else:
            print(
                'Incorrect iata code. Please, '
                'enter a correct iata code("{}" '
                'or "{}" or "{}")'.format(
                    iata_code[0], iata_code[1], iata_code[2]
                )
            )
            dep_city = input('Please, enter IATA code of departure city: ')

    # Checking and input IATA code of arrival airport

    while True:
        if arr_city is None:
            arr_city = input(
                'Please, enter IATA '
                'code of arrival city: '
            ).upper()
        else:
            arr_city = arr_city.upper()

        if arr_city in iata_code:
            break
        else:
            print(
                'Incorrect iata code. Please, '
                'enter a correct iata code("{}" '
                'or "{}" or "{}")'.format(
                    iata_code[0], iata_code[1], iata_code[2]
                )
            )
            arr_city = input('Please, enter IATA code of arrival city: ')

    # Input and checking for correctness departure date

    while True:
        try:
            if dep_date is None:
                dep_date = input(
                    'Please, enter a departure'
                    ' date(dd/mm/yyyy): '
                )
            dep_date = re.findall(r'(\d|\d{2}).(\d{2}).(\d{4})', dep_date)[0]
            if datetime.date(
                    int(dep_date[2]),
                    int(dep_date[1]),
                    int(dep_date[0])
            ):
                break
        except (IndexError, TypeError, ValueError):
            print(
                'Incorrect date. Please, enter a '
                'correct date in format: day/month/year'
            )
            dep_date = input('Please, enter a departure date(dd/mm/yyyy): ')
    # Input and checking for correctness return date

    while True:
        if way == 'ONE_WAY':
            ret_date = dep_date
            break
        elif way == 'ROUND_TRIP':
            try:
                if ret_date is None:
                    ret_date = input(
                        'Please, enter a return'
                        ' date(dd/mm/yyyy): '
                    )
                ret_date = re.findall(
                    r'(\d|\d{2}).(\d{2}).(\d{4})',
                    ret_date
                )[0]

                if datetime.date(
                        int(ret_date[2]),
                        int(ret_date[1]),
                        int(ret_date[0])
                ):
                    break
            except (IndexError, TypeError, ValueError):
                print(
                    'Incorrect date. Please, enter a '
                    'correct date in format: day/month/year'
                )
                ret_date = input('Please, enter a return date(dd/mm/yyyy): ')
    # checking number of adults

    while True:
        if adults is None:
            adults = input(
                'Please, enter a number of adults'
                '(number must be more than 0 and less or equal 9): '
            )
        try:
            adults = int(adults)
            if adults <= 0 or adults >= 9:
                print(
                    'Number of adults must be more '
                    'or equal 1 and less or equal 9.'
                )

            else:
                break
        except (ValueError, TypeError):
            print('Number of adults must be integer.')
        adults = input(
            'Please, enter a number of adults'
            '(number must be more than 0 and less or equal 9): '
        )

    # checking number of children

    while True:
        if children is None:
            children = input(
                'Please, enter a number of children'
                '(number must be more or equal than '
                '0 and less or equal number of adults): '
            )
        try:
            children = int(children)
            if children < 0 or children > adults or children + adults > 9:
                print(
                    'Number of children must be more or equal '
                    '0 and less or equal number of adults, '
                    'and sum of number of adults and '
                    'children must not be more 9.'
                )
            else:
                break
        except (ValueError, TypeError):
            print('Number of children must be integer number.')
        children = input(
            'Please, enter a number of children'
            '(number must be more or equal than '
            '0 and less or equal number of adults): '
        )

    # checking number of infants

    while True:
        if infants is None:
            infants = input(
                'Please, enter a number of infants'
                '(number must be more or equal than '
                '0 and less or equal number of adults): '
            )
        try:
            infants = int(infants)
            if infants < 0 or infants > adults or infants > 5:
                print(
                    'Number of infants must be more or equal '
                    '0 and less or equal number of adults.'
                )
            else:
                break
        except (ValueError, TypeError):
            print('Number of children must be integer number.')
        infants = input(
            'Please, enter a number of infants'
            '(number must be more or equal than '
            '0 and less or equal number of adults): '
        )
    return (
        way, dep_city, arr_city,
        '/'.join(dep_date), '/'.join(ret_date),
        adults, children, infants
    )


def connection(params_func):
    """Function gets params of searching and set connection with site."""

    params = {
        'buscadorVuelosEsb.tipoTransicion': 'S',
        'buscadorVuelosEsb.routeType': params_func[0],
        'buscadorVuelosEsb.origen': params_func[1],
        'buscadorVuelosEsb.destino': params_func[2],
        'buscadorVuelosEsb.fsalida': params_func[3],
        'buscadorVuelosEsb.fregreso': params_func[4],
        'buscadorVuelosEsb.numadultos': params_func[5],
        'buscadorVuelosEsb.numninos': params_func[6],
        'buscadorVuelosEsb.numbebes': params_func[7]
    }
    tree = html.fromstring(
        requests.post(
            'https://en.orbest.com/b2c'
            '/pages/flight/disponibili'
            'dadSubmit.html?', params
        ).content
    )
    return tree


def scrape(connect_func, params_func):
    """Gets data from site."""

    params = params_func
    tree = connect_func
    flights = [[], []]  # List of vars of flights
    # (first lis for outbound flights, second list for return flight)
    if params[0] == 'ONE_WAY':
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

    elif params[0] == 'ROUND_TRIP':
        data = tree.xpath(               # Getting data of outbound flights
            '/html/body/div[@id="content"]'
            '/div/div/form[@id="formularioValoracion"]'
            '/div/div[@class="flexcols"]/section'
            '/div[@id="tabs2"]/div/div'
            '/div[@class="wrap-sel-custom combinado"]'
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

            flight_last = ' '.join(
                details.xpath(
                    'div[@class="col2 col-last"]'
                    '/div[@class="datos"]/div//text()'
                )
            )  # Getting data of return flights

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


def time_difference(data_func, params_func):
    """Calculating of flight time."""

    way = params_func[0]
    data = data_func
    flights_time = [[], []]
    if way == 'ONE_WAY':
        flights_time.clear()
        for flight in data:
            dep_time = re.findall(
                r'\d{1,2}:\d{2}', ' '.join(flight)
            )[0].split(':')
            dep_hour = float(dep_time[0])
            dep_minutes = float(dep_time[1])
            arr_time = re.findall(
                r'\d{1,2}:\d{2}', ' '.join(flight)
            )[1].split(':')
            arr_hour = float(arr_time[0])
            arr_minutes = float(arr_time[1])
            dep_flight_time = datetime.timedelta(
                hours=dep_hour, minutes=dep_minutes
            )
            arr_flight_time = datetime.timedelta(
                hours=arr_hour, minutes=arr_minutes
            )
            flights_time.append(arr_flight_time - dep_flight_time)
    elif way == 'ROUND_TRIP':
        for i, _ in enumerate(flights_time):
            for flight in data[i]:
                dep_time = re.findall(
                    r'\d{1,2}:\d{2}', ' '.join(flight)
                )[0].split(':')
                dep_hour = float(dep_time[0])
                dep_minutes = float(dep_time[1])
                arr_time = re.findall(
                    r'\d{1,2}:\d{2}', ' '.join(flight)
                )[1].split(':')
                arr_hour = float(arr_time[0])
                arr_minutes = float(arr_time[1])
                dep_flight_time = datetime.timedelta(
                    hours=dep_hour, minutes=dep_minutes
                )
                arr_flight_time = datetime.timedelta(
                    hours=arr_hour, minutes=arr_minutes
                )
                flights_time[i].append(arr_flight_time - dep_flight_time)
    return flights_time


def data_print(data_func, params_func, time_dif):
    """Result printing."""

    time = time_dif
    if data_func == list() or data_func == [[], []]:
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )
    else:
        if params_func[0] == 'ONE_WAY':
            for i, _ in enumerate(data_func):
                print('Way:', data_func[i][3])
                print('Departure time:', data_func[i][5])
                print('Arrival time:', data_func[i][7])
                print('Class:', data_func[i][9])
                print('Price:', data_func[i][0])
                print('Flight duration:', time[i])
                print('\n')
        elif params_func[0] == 'ROUND_TRIP':
            print('Outbound flights', '\n')
            for info in data_func[0]:
                print('Way: {0}-{1}'.format(info[0], info[1]))
                print('Departure time:', info[4])
                print('Arrival time:', info[5])
                print('Class:', info[2])
                print('Price:', info[3])
                print('Flight duration:', time[0][data_func[0].index(info)])
                print('\n')
            print('Return flights', '\n')
            for inform in data_func[1]:
                print('Way: {0}-{1}'.format(inform[0], inform[1]))
                print('Departure time:', inform[4])
                print('Arrival time:', inform[5])
                print('Class:', inform[2])
                print('Price:', inform[3])
                print('Flight duration:', time[1][data_func[1].index(inform)])
                print('\n')


if __name__ == '__main__':
    counter = 0
    query_params = input_query_params()
    while True:
        parameters = manual_input(counter)
        connect = connection(parameters)
        data_flights = scrape(connect, parameters)
        flight_time = time_difference(data_flights, parameters)
        data_print(data_flights, parameters, flight_time)
        counter += 1
        if input('For quit enter "q"').upper() == 'Q':
            break
