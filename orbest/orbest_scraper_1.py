"""Python 3.7. Parsing of the web site https://www.orbest.com/."""


import argparse
import datetime
import re
import requests

from lxml import html


def check_flight_type(way):
    """Check that flight type is valid."""

    try:
        way = way.upper()
    except AttributeError:
        return False
    if way in {'ONE_WAY', 'ROUND_TRIP'}:
        return True
    print(
        'Incorrect flight type. Please, '
        'enter a correct one(ONE_WAY/ROUND_TRIP).'
    )

    return False


def check_cities(dep_city, arr_city):
    """Check that IATA codes are valid."""

    try:
        dep_city = dep_city.upper()
        arr_city = arr_city.upper()
    except AttributeError:
        return False
    if dep_city not in AVAILABLE_ROUTES:
        print('Incorrect departure city.')
        return False
    elif arr_city not in AVAILABLE_ROUTES:
        print('Incorrect arrival city.')
        return False
    elif dep_city == arr_city:
        print("Departure city mustn't be same arrival city.") #google
        return False

    return True


def check_dates(*dates): # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """Check if dates are valid."""

    checked_dates = []
    try:
        for date in dates:
            try:
                date = re.findall(r'(\d|\d{2}).(\d{2}).(\d{4})', date)[0] # начало и конец строки, ексепшны
            except IndexError:
                pass
            date = datetime.date(int(date[2]), int(date[1]), int(date[0]))
            today = datetime.datetime.now()
            today = datetime.date(today.year, today.month, today.day)
            if not date:
                print('Incorrect date')
                return False
            if date <= today:
                print('You must choose a future date.')
                return False
            if date and date >= today:
                checked_dates.append(date)
        if checked_dates[0] > checked_dates[1]:
            print("Departure date mustn't be more than return date.")
            return False

        return True

    except (IndexError, TypeError, ValueError):
        print(
            'Incorrect date. Please, enter a '
            'correct date in format: day/month/year'
        )
        return False


def check_passengers(adults, children, infants):
    """Check number of passengers."""

    try:
        adults = int(adults)
    except (ValueError, TypeError):
        print('Number of adults must be integer number.')
        return False

    if adults <= 0 or adults > 9: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(
            'Number of adults must be more '
            'or equal 1 and less or equal 9.'
        )
        return False

    try:
        children = int(children)
        if children < 0 or children + adults > 9:
            print('Number of children must be more or equal 0 '
                  'and less or equal number of adults, and '
                  'sum of number of adults and children must '
                  'not be more than 9.')
            return False
    except (ValueError, TypeError): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! gthtytcnb
        print('Number of children must be integer number.')
        return False

    try:
        infants = int(infants)
        if infants < 0 or infants > adults or infants > 5:
            print('Number of infants must be more or equal '
                  '0 and less or equal number of adults.')
            return False
    except (ValueError, TypeError):
        print('Number of infants must be integer number.')
        return False

    return True


def get_query_params_from_command_line():
    """Parse and check arguments of command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-w', '--way', help='input way type("ONE_WAY" or "ROUND_TRIP")')
    parser.add_argument(
        '-d', '--dep_city', help='input departure city("LIS", "CUN", "PUJ")')
    parser.add_argument(
        '-a', '--arr_city',  help='input arrival city("LIS", "CUN", "PUJ")')
    parser.add_argument('-d_d', '--dep_date', help='input a departure date')
    parser.add_argument('-r', '--ret_date', help='input a return date')
    parser.add_argument(
        '-n_a', '--num_adults', help='input a number of adults')
    parser.add_argument(
        '-n_c', '--num_child',   help='input a number of children')
    parser.add_argument(
        '-n_i', '--num_infants',  help='input a number of infants')

    args = parser.parse_args()

    if not check_flight_type(args.way):
        return None

    if not check_cities(args.dep_city, args.arr_city):
        return None

    if not check_dates(args.dep_date, args.ret_date):
        return None

    if not check_passengers(args.num_adults, args.num_child, args.num_infants):
        return None

    args.way = args.way.upper()
    args.dep_city = args.dep_city.upper()
    args.arr_city = args.arr_city.upper()

    if args.way == 'ONE_WAY':
        args.ret_date = args.dep_date

    return {
        'flight_type': args.way, 'dep_city': args.dep_city,
        'arr_city': args.arr_city, 'dep_date': args.dep_date,
        'ret_date': args.ret_date, 'adults': args.num_adults,
        'children': args.num_child, 'infants': args.num_infants
    }


def manual_input():
    """Get query params from manual input."""

    while True:
        flight_type = input(
            'Please, enter type of flight'
            '("ONE_WAY" or "ROUND_TRIP"): '
        ).upper()

        if check_flight_type(flight_type):
            break

    while True:
        dep_city = input(
            'Please, enter IATA '
            'code of departure city({}): '.format(
                ', '.join(AVAILABLE_ROUTES)
            )
        ).upper()

        arr_city = input(
            'Please, enter IATA '
            'code of arrival city({}): '.format(
                ', '.join(AVAILABLE_ROUTES)
            )
        ).upper()

        if check_cities(dep_city, arr_city):
            break

    while True:
        dep_date = input(
            'Please, enter '
            'departure date(dd/mm/yyyy): '
        ).upper()

        if flight_type == 'ROUND_TRIP':
            ret_date = input('Please, enter return date(dd/mm/yyyy): ')
        else:
            ret_date = dep_date

        if check_dates(dep_date, ret_date):
            break

    while True:
        adults = input(
            'Please, enter a number of adults'
            '(number must be more than 0 and less or equal 9): '
        )
        children = input(
            'Please, enter a number of children'
            '(number must be more or equal than 0 '
            'and less or equal number of adults): '
        )
        infants = input(
            'Please, enter a number of infants'
            '(number must be more or equal than 0 '
            'and less or equal number of adults): '
        )

        if check_passengers(adults, children, infants):
            break

    return {
        'flight_type': flight_type, 'dep_city': dep_city, 'arr_city': arr_city,
        'dep_date': dep_date, 'ret_date': ret_date, 'adults': adults,
        'children': children, 'infants': infants
    }


def get_available_routes():
    """Create list of available routes."""

    response = requests.get('https://en.evelop.com/').content
    routes_json = re.findall(r'routesWebSale = {(.+)}', str(response))[0] #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! JSON
    # cities = list(set(re.findall(r'\b[A-Z]{3}\b', res)))
    return routes_json


def get_data_page(search_params):
    """Getting html page from web-site."""

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
            'https://en.evelop.com/b2c'
            '/pages/flight/disponibili'
            'dadSubmit.html?', params
        ).content
    )

    data = tree.xpath(
        '/html/body/div[@id="content"]'
        '/div/div/form[@id="formularioValoracion"]'
        '/div/div[@class="flexcols"]/section'
        '/div[@id="tabs2"]/div/div'
    )

    return data


def parse_results(data_page, *args):

    def parse_results_for_one_way(data_page):
        """Getting data about flights for "one way" flight type."""

        try:
            data = data_page[0].xpath('ol/li')
            flights = [  # List of lists of flights
                information.xpath(
                    'div[@class="vuelo-wrap'
                    ' vuelo-wrap3"]//text()'
                ) for information in data
            ]
        except IndexError:    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            flights = []
        return flights

    def parse_results_for_round_trip(data_page):
        """Getting data about flights for "round trip" flight type."""

        try:
            data = data_page[0].xpath(  # Getting data of outbound flights
                'div[@class="wrap-sel-custom combinado"]'
                '/div[@class="grid-cols clearfix"]'
            )
            flights = []
            for details in data:
                flight_first = details.xpath(
                    'div[@class="col2 col-first"]'
                    '/div[@class="datos"]/div//text()'
                )
                # Getting data of departure flights
                flights.append(flight_first)
                flight_last = details.xpath(
                    'div[@class="col2 col-last"]'
                    '/div[@class="datos"]/div//text()'
                )
                flights = [flight_first, flight_last]
        except IndexError:
            flights = []

        return flights

    return parse_results_for_one_way(data_page) if args[0] == 'ONE_WAY' \
        else parse_results_for_round_trip(data_page)

def generate_quotes(data):
    pass


def scrape(search_params):
    """Get search params if necessary and return quotes."""

    if not search_params:
        search_params = manual_input()

    data_page = get_data_page(search_params)
    data = parse_results(data_page, search_params['flight_type'] )
    quotes = generate_quotes(data)
    # if search_params['flight_type'] == 'ONE_WAY':
    #     data = get_results_for_one_way(data_page)
    #     time_dif = []
    #     for flight in data:
    #         dep_time = re.findall(r'\d{1,2}:\d{2}',
    #                               ' '.join(flight))[0].split(':')
    #         arr_time = re.findall(r'\d{1,2}:\d{2}',
    #                               ' '.join(flight))[1].split(':')
    #         dep_time = datetime.timedelta(hours=float(dep_time[0]),
    #                                       minutes=float(dep_time[1]))
    #         arr_time = datetime.timedelta(hours=float(arr_time[0]),
    #                                       minutes=float(arr_time[1]))
    #         time_dif.append(re.search(r'\d{1,2}:\d{2}',
    #                                   str(arr_time - dep_time))[0])
    #     for i, _ in enumerate(time_dif):
    #         data[i].insert(0, time_dif[i])
    #     flight_list = [[]]
    #     for flight in data:
    #         dep_city = re.findall(r'\w{3}', flight[4])[0]
    #         arr_city = re.findall(r'\w{3}', flight[4])[1]
    #         price = flight[1]
    #         dep_time = flight[6]
    #         arr_time = flight[8]
    #         flight_time = flight[0]
    #         flight_class = flight[10]
    #         flight = [dep_city, arr_city, price, dep_time,
    #                   arr_time, flight_time, flight_class]
    #         flight_list[0].append(flight)
    # else:
    #     data = get_results_for_round_trip(data_page)
    #     flight_list = [[], []]
    #     for i, _ in enumerate(data):
    #         cities = re.findall(r'[A-Z]{3}', ''.join(data[i]))
    #         cities = [cities[i:i + 2] for i in
    #                   range(0, len(cities), 2)][:len(cities) // 4]
    #         price = re.findall(r'.\d+,\d{2}', ''.join(data[i]))
    #         time = re.findall(r'\d{1,2}:\d{2}', ''.join(data[i]))
    #         time = [time[l:l + 2] for l in
    #                 range(0, len(time), 2)][:len(time) // 4]
    #         flight_class = re.findall(r'Promotional|Economic|Standard|'
    #                                   r'Flexible\sPlus|Flexible|Plena',
    #                                   ''.join(data[i]))
    #         time_dif = []
    #         for j, _ in enumerate(time):
    #             dep_time = time[j][0].split(':')
    #             arr_time = time[j][1].split(':')
    #             dep_time = datetime.timedelta(hours=float(dep_time[0]),
    #                                           minutes=float(dep_time[1]))
    #             arr_time = datetime.timedelta(hours=float(arr_time[0]),
    #                                           minutes=float(arr_time[1]))
    #             time_dif.append(re.search(r'\d{1,2}:\d{2}',
    #                                       str(arr_time - dep_time))[0])
    #         for k, _ in enumerate(price):
    #             dep_city = cities[k][0]
    #             arr_city = cities[k][1]
    #             flight = [dep_city, arr_city, price[k], time[k][0],
    #                       time[k][1], time_dif[k], flight_class[k]]
    #             flight_list[i].append(flight)

    return quotes


def print_result(result_func):
    """Printing results."""

    for i, _ in enumerate(result_func):
        list_for_print_result = ['Outbound flights', 'Return flights']
        if result_func == [[]] or result_func == [[], []]:
            print(
                'There is not availability enough '
                'for the selected flights. Please '
                'select another date.'
            )
            break
        else:
            print(list_for_print_result[i], '\n')
            for info in result_func[i]:
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


if __name__ == '__main__':
    AVAILABLE_ROUTES = get_available_routes()
    query_params = get_query_params_from_command_line()
    while True:
        result_data = scrape(query_params)
        print_result(result_data)
        query_params = None
        if input(
            'Enter "EXIT" to close program. '
            'For continue press "Enter".'
        ).upper() == 'EXIT':
            break
