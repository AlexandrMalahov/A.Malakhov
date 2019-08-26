"""Python 3.7. Parsing of the web site https://www.orbest.com/."""


import argparse
import datetime
import re
import requests

from lxml import html


def check_flight_type(way):
    try:
        way = way.upper()
    except AttributeError:
        return False
    if way in {'ONE_WAY', 'ROUND_TRIP'}:
        return True
    else:
        print('Incorrect flight type. Please, enter a correct way.')
        return False


def check_cities(dep_city, arr_city):
    iata_code = ['LIS', 'CUN', 'PUJ']
    try:
        dep_city = dep_city.upper()
        arr_city = arr_city.upper()
    except AttributeError:
        return False
    if dep_city not in iata_code:

        print('Incorrect departure city.')
        return False
    elif arr_city not in iata_code:
        print('Incorrect arrival city.')
        return False
    elif dep_city == arr_city:
        print("Departure city mustn't be same arrival city.")
        return False
    else:
        return True


def check_dates(dep_date, ret_date):
    dates = [dep_date, ret_date]
    checked_dates = []
    try:
        for date in dates:
            date = re.findall(r'(\d|\d{2}).(\d{2}).(\d{4})', date)[0]
            date = datetime.date(int(date[2]), int(date[1]), int(date[0]))
            today = datetime.datetime.now()
            today = datetime.date(today.year, today.month, today.day)
            if not date:
                print('Incorrect date')
                return False
            if date and date >= today:
                checked_dates.append(date)
        if checked_dates[0] > checked_dates[1]:
            print("Departure date mustn't be more return date.")
            return False
        else:
            return True
    except (IndexError, TypeError, ValueError):
        print(
            'Incorrect date. Please, enter a '
            'correct date in format: day/month/year'
        )
        return False


def check_passengers(adults, children, infants):
    try:
        adults = int(adults)
        if adults <= 0 or adults >= 9:
            print(
                'Number of adults must be more '
                'or equal 1 and less or equal 9.'
            )
            return False
    except (ValueError, TypeError):
        print('Number of adults must be integer number.')
        return False

    try:
        children = int(children)
        if children < 0 or children + adults > 9:
            print(
                'Number of children must be more or equal '
                '0 and less or equal number of adults, '
                'and sum of number of adults and '
                'children must not be more 9.'
            )
            return False
    except (ValueError, TypeError):
        print('Number of children must be integer number.')
        return False

    try:
        infants = int(infants)
        if infants < 0 or infants > adults or infants > 5:
            print(
                'Number of infants must be more or equal '
                '0 and less or equal number of adults.'
            )
            return False
    except (ValueError, TypeError):
        print('Number of infants must be integer number.')
        return False

    return True


def get_query_params_from_command_line():
    """Parsing arguments of command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--way',
                        help='input way type("ONE_WAY" or "ROUND_TRIP")')
    parser.add_argument('-d', '--dep_city',
                        help='input departure city("LIS", "CUN", "PUJ")')
    parser.add_argument('-a', '--arr_city',
                        help='input arrival city("LIS", "CUN", "PUJ")')
    parser.add_argument('-d_d', '--dep_date', help='input a departure date')
    parser.add_argument('-r', '--ret_date', help='input a return date')
    parser.add_argument('-n_a', '--num_adults',
                        help='input a number of adults')
    parser.add_argument('-n_c', '--num_child',
                        help='input a number of children')
    parser.add_argument('-n_i', '--num_infants',
                        help='input a number of infants')
    args = parser.parse_args()

    if not check_flight_type(args.way):
        return None
    else:
        args.way = args.way.upper()

    if not check_cities(args.dep_city, args.arr_city):
        return None
    else:
        args.dep_city = args.dep_city.upper()
        args.arr_city = args.arr_city.upper()

    if args.way == 'ONE_WAY':
        args.ret_date = args.dep_date
    if not check_dates(args.dep_date, args.ret_date):
        return None

    if not check_passengers(args.num_adults, args.num_child, args.num_infants):
        return None

    cl_args = {'flight_type': args.way, 'dep_city': args.dep_city, 'arr_city': args.arr_city,
            'dep_date': args.dep_date, 'ret_date': args.ret_date, 'adults': args.num_adults,
            'children': args.num_child, 'infants': args.num_infants}

    return cl_args


def manual_input():
    while True:
        way = input('Please, enter type of flight'
                    '("ONE_WAY" or "ROUND_TRIP"): ').upper()
        if check_flight_type(way):
            break

    while True:
        dep_city = input('Please, enter IATA '
                         'code of departure city: ').upper()
        arr_city = input('Please, enter IATA '
                         'code of arrival city: ').upper()
        if check_cities(dep_city, arr_city):
            break

    while True:
        dep_date = input('Please, enter a departure date(dd/mm/yyyy): ').upper()
        if way == 'ROUND_TRIP':
            ret_date = input('Please, enter a return date(dd/mm/yyyy): ')
        else:
            ret_date = dep_date
        if check_dates(dep_date, ret_date):
            break

    while True:
        adults = input('Please, enter a number of adults'
                       '(number must be more than 0 and less or equal 9): ')
        children = input('Please, enter a number of children(number must be '
                         'more or equal than 0 and less or equal number of adults): ')
        infants = input('Please, enter a number of infants(number must be '
                        'more or equal than 0 and less or equal number of adults): ')
        if check_passengers(adults, children, infants):
            break

    return {'flight_type': way, 'dep_city': dep_city, 'arr_city': arr_city,
            'dep_date': dep_date, 'ret_date': ret_date, 'adults': adults,
            'children': children, 'infants': infants}


def get_data_page(search_params):

    params = {
        'buscadorVuelosEsb.tipoTransicion': 'S',
        'buscadorVuelosEsb.routeType': search_params['flight_type'],
        'buscadorVuelosEsb.origen': search_params['dep_city'],
        'buscadorVuelosEsb.destino': search_params['arr_city'],
        'buscadorVuelosEsb.fsalida': search_params['dep_date'],
        'buscadorVuelosEsb.fregreso': search_params['ret_date'],
        'buscadorVuelosEsb.numadultos': search_params['adults'],
        'buscadorVuelosEsb.numninos': search_params['children'],
        'buscadorVuelosEsb.numbebes': search_params['infants']
    }

    tree = html.fromstring(
        requests.post(
            'https://en.orbest.com/b2c'
            '/pages/flight/disponibili'
            'dadSubmit.html?', params
        ).content
    )

    return tree


def get_results_for_one_way(data_page):

    tree = data_page
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
    time_dif = []
    for flight in flights:
        dep_time = re.findall(r'\d{1,2}:\d{2}', ' '.join(flight))[0].split(':')
        arr_time = re.findall(r'\d{1,2}:\d{2}', ' '.join(flight))[1].split(':')
        dep_time = datetime.timedelta(hours=float(dep_time[0]), minutes=float(dep_time[1]))
        arr_time = datetime.timedelta(hours=float(arr_time[0]), minutes=float(arr_time[1]))
        time_dif.append(arr_time - dep_time)
    for i, _ in enumerate(time_dif):
        flights[i].insert(0, time_dif[i])
    return flights


def get_results_for_round_trip(data_page):
    tree = data_page
    data = tree.xpath(  # Getting data of outbound flights
        '/html/body/div[@id="content"]'
        '/div/div/form[@id="formularioValoracion"]'
        '/div/div[@class="flexcols"]/section'
        '/div[@id="tabs2"]/div/div'
        '/div[@class="wrap-sel-custom combinado"]'
        '/div[@class="grid-cols clearfix"]'
    )

    flights_list = [[], []]
    for details in data:
        flight_first = details.xpath(
                'div[@class="col2 col-first"]'
                '/div[@class="datos"]/div//text()'
            )
          # Getting data of departure flights

        flight_last = details.xpath(
                'div[@class="col2 col-last"]'
                '/div[@class="datos"]/div//text()'
            )

        first_fly_class = details.xpath(
            'div[@class="col2 col-first"]'
            '/div[@class="datos"]/div'
            '/div[@class="clase"]/span//text()'
        )
        second_fly_class = details.xpath(
            'div[@class="col2 col-last"]'
            '/div[@class="datos"]/div'
            '/div[@class="clase"]/span//text()'
        )

        fly_class = first_fly_class, second_fly_class
        flights = [flight_first, flight_last]

        for i, _ in enumerate(flights):
            flight = []
            cities = re.findall(r'\b\w{3}\b', ' '.join(flights[i]))[:2]
            price = re.findall(r'.\d+,\d{2}', ' '.join(flights[i]))
            time = re.findall(r'\d{1,2}:\d{2}', ' '.join(flights[i]))
            time = [time[i:i + 2] for i in range(0, len(time), 2)][:len(price)]
            time_dif = []
            for j, _ in enumerate(time):
                dep_time = time[j][0].split(':')
                arr_time = time[j][1].split(':')
                dep_time = datetime.timedelta(hours=float(dep_time[0]), minutes=float(dep_time[1]))
                arr_time = datetime.timedelta(hours=float(arr_time[0]), minutes=float(arr_time[1]))
                time_dif.append(arr_time - dep_time)
            for k, _ in enumerate(price):
                fly = [cities[0], cities[1], price[k], time[k][0], time[k][1], time_dif[k], fly_class[i][k]]
                flight.append(fly)
            flights_list[i] = flight

        return flights_list


def print_one_way_result(one_way_func):
    data = one_way_func
    if data == []:
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )
    else:
        for info in data:
            way = info[4]
            price = info[1]
            dep_time = info[6]
            arr_time = info[8]
            flight_time = info[0]
            flight_class = info[10]
            print('Way:', way)
            print('Price:', price)
            print('Departure time', dep_time)
            print('Arrival time:', arr_time)
            print('Flight time:', flight_time)
            print('Flight class:', flight_class)
            print('\n')


def print_round_trip_result(round_trip_func):
    data = round_trip_func
    list_for_print_result = ['Outbound flights', 'Return flights']
    if data == [[], []]:
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )
    else:
        for i, _ in enumerate(data):
            print(list_for_print_result[i], '\n')
            for info in data[i]:
                way = info[0] + '-' + info[1]
                price = info[2]
                dep_time = info[3]
                arr_time = info[4]
                flight_time = info[5]
                flight_class = info[6]
                print('Way:', way)
                print('Price:', price)
                print('Departure time', dep_time)
                print('Arrival time:', arr_time)
                print('Flight time:', flight_time)
                print('Flight class:', flight_class)
                print('\n')


if __name__ == "__main__":
    query_params = get_query_params_from_command_line()
    if not query_params:
        query_params = manual_input()
    while True:
        data_page = get_data_page(query_params)
        result_data = print_one_way_result(get_results_for_one_way(data_page)) \
            if query_params['flight_type'] == 'ONE_WAY' \
            else print_round_trip_result(get_results_for_round_trip(data_page))
        escape = input('Enter "EXIT" to close program. For continue press "Enter".').upper()
        if escape == 'EXIT':
            break
        query_params = manual_input()
