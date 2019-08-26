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
            'dep_date': args.dep_date, 'ret_date': args.ret_date, 'adults': args.adults,
            'children': args.children, 'infants': args.infants}

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
    outbound_flight = []
    ret_flight = []
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
        time = [time[i:i + 2] for i in range(0, len(time), 2)]

        for i, class_type in enumerate(fly_class):
            outbound_flight.append(
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
        time = [time[i:i + 2] for i in range(0, len(time), 2)]

        for i, class_type in enumerate(fly_class):
            ret_flight.append([
                cities[0],
                cities[1],
                class_type,
                price[i],
                time[i][0],
                time[i][1]
            ])
    return outbound_flight, ret_flight

# def scrape(search_params):
#     """Gets data from site."""
#
#     if not search_params:
#         search_params = manual_input()
#
#     data_page = get_data_page(search_params)
#     result_data = get_results_for_one_way() if way =='ONE_WAY' else get_results_for_round_trip()
#     result_data = time_difference(result_data)
#     return result_data


# def time_difference(data_func, params_func):
#     """Calculating of flight time."""
#
#     way = params_func[0]
#     data = data_func
#     flights_time = [[], []]
#     if way == 'ONE_WAY':
#         flights_time.clear()
#         for flight in data:
#             dep_time = re.findall(
#                 r'\d{1,2}:\d{2}', ' '.join(flight)
#             )[0].split(':')
#             dep_hour = float(dep_time[0])
#             dep_minutes = float(dep_time[1])
#             arr_time = re.findall(
#                 r'\d{1,2}:\d{2}', ' '.join(flight)
#             )[1].split(':')
#             arr_hour = float(arr_time[0])
#             arr_minutes = float(arr_time[1])
#             dep_flight_time = datetime.timedelta(
#                 hours=dep_hour, minutes=dep_minutes
#             )
#             arr_flight_time = datetime.timedelta(
#                 hours=arr_hour, minutes=arr_minutes
#             )
#             flights_time.append(arr_flight_time - dep_flight_time)
#     elif way == 'ROUND_TRIP':
#         for i, _ in enumerate(flights_time):
#             for flight in data[i]:
#                 dep_time = re.findall(
#                     r'\d{1,2}:\d{2}', ' '.join(flight)
#                 )[0].split(':')
#                 dep_hour = float(dep_time[0])
#                 dep_minutes = float(dep_time[1])
#                 arr_time = re.findall(
#                     r'\d{1,2}:\d{2}', ' '.join(flight)
#                 )[1].split(':')
#                 arr_hour = float(arr_time[0])
#                 arr_minutes = float(arr_time[1])
#                 dep_flight_time = datetime.timedelta(
#                     hours=dep_hour, minutes=dep_minutes
#                 )
#                 arr_flight_time = datetime.timedelta(
#                     hours=arr_hour, minutes=arr_minutes
#                 )
#                 flights_time[i].append(arr_flight_time - dep_flight_time)
#     return flights_time


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





if __name__ == "__main__":
    query_params = manual_input()
    data_page = get_data_page(query_params)

    result_data = get_results_for_one_way(data_page) \
        if query_params['flight_type'] == 'ONE_WAY' \
        else get_results_for_round_trip(data_page)
    print(result_data)





