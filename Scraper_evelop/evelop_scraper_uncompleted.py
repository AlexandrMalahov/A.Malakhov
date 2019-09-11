"""Python 3.7. Parsing of the web site https://www.orbest.com/."""


import argparse
import datetime
import json
import re
import requests

import evelop_sql

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


def check_cities(dep_city, arr_city, routes):
    """Check that IATA codes are valid."""


    try:
        dep_city = dep_city.upper()
        arr_city = arr_city.upper()
    except AttributeError:
        return False
    if dep_city not in routes:
        print('Incorrect departure city.')
        return False
    elif arr_city not in routes:
        print('Incorrect arrival city.')
        return False
    elif arr_city not in routes[dep_city]:
        print('No such routes.')
        print('Available routes: ')
        for route in routes:
            print(route, 'to', routes[route])
        return False
    elif dep_city == arr_city:
        print("Departure city mustn't be same arrival city.")
        return False

    return True


def check_dates(*dates):
    """Check if dates are valid."""

    checked_dates = []

    for date in dates:
        try:
            date = re.findall(r'\b(\d{1,2})\W(\d{2})\W(\d{4})\b', date)[0]
        except IndexError:
            print('Incorrect date.')
            return False
        except TypeError:
            print('You did not enter a date.')
            return False
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


def check_passengers(adults, children, infants):
    """Check number of passengers."""

    try:
        adults = int(adults)
    except ValueError:
        print('Number of adults must be integer number.')
        return False
    except TypeError:
        print('You did not enter number of adults.')
        return False

    if adults <= 0 or adults > 9:
        print(
            'Number of adults must be more '
            'or equal 1 and less or equal 9.'
        )
        return False

    try:
        children = int(children)
    except ValueError:
        print('Number of children must be integer number.')
        return False
    except TypeError:
        print('You did not enter number of children.')
        return False
    if children < 0 or children + adults > 9:
        print('Number of children must be more or equal 0 '
              'and less or equal number of adults, and '
              'sum of number of adults and children must '
              'not be more than 9.')
        return False

    try:
        infants = int(infants)
    except ValueError:
        print('Number of infants must be integer number.')
        return False
    except TypeError:
        print('You did not enter number of infants.')
        return False
    if infants < 0 or infants > adults or infants > 5:
        print('Number of infants must be more or equal '
              '0 and less or equal number of adults.')
        return False

    return True


def get_query_params_from_command_line():
    """Parse and check arguments of command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--flight_type', help='input way type("ONE_WAY" or "ROUND_TRIP")'
    )
    parser.add_argument(
        '-d', '--dep_city', help='input departure city("LIS", "CUN", "PUJ")'
    )
    parser.add_argument(
        '-a', '--arr_city',  help='input arrival city("LIS", "CUN", "PUJ")'
    )
    parser.add_argument('-d_d', '--dep_date', help='input a departure date')
    parser.add_argument('-r', '--ret_date', help='input a return date')
    parser.add_argument(
        '-n_a', '--num_adults', help='input a number of adults'
    )
    parser.add_argument(
        '-n_c', '--num_child',   help='input a number of children'
    )
    parser.add_argument(
        '-n_i', '--num_infants',  help='input a number of infants'
    )

    args = parser.parse_args()

    if not check_flight_type(args.flight_type):
        return None

    if not check_cities(args.dep_city, args.arr_city, AVAILABLE_ROUTES):
        return None

    if args.flight_type == 'ONE_WAY' or args.flight_type == 'one_way':
        args.ret_date = args.dep_date
    if not check_dates(args.dep_date, args.ret_date):
        return None

    if not check_passengers(args.num_adults, args.num_child, args.num_infants):
        return None

    return {
        'flight_type': args.flight_type.upper(),
        'dep_city': args.dep_city.upper(),
        'arr_city': args.arr_city.upper(), 'dep_date': args.dep_date,
        'ret_date': args.ret_date, 'adults': args.num_adults,
        'children': args.num_child, 'infants': args.num_infants
    }


def manual_input(routes):
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
                ', '.join(routes)
            )
        ).upper()

        arr_city = input(
            'Please, enter IATA '
            'code of arrival city({}): '.format(
                ', '.join(routes)
            )
        ).upper()

        if check_cities(dep_city, arr_city, routes):
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

    response = requests.get('https://en.evelop.com/', verify=False).content

    routes_json = re.findall(r'routesWebSale = ({.+});', str(response))[0]
    routes = re.split(r';', routes_json)[0]
    routes_json = json.loads(routes)

    return routes_json


def parameters(search_params):
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

    return params


def get_data_page(search_params):
    """Get html page from web-site."""

    params = parameters(search_params)
    tree = html.fromstring(
        requests.post(
            'https://en.evelop.com/b2c'
            '/pages/flight/disponibili'
            'dadSubmit.html?', params, verify=False
        ).content
    )

    return tree


def get_price(get_params):

    params = parameters(QUERY_PARAMS)
    session = requests.session()
    post_request = session.post(
        'https://en.evelop.com/b2c'
        '/pages/flight/disponibili'
        'dadSubmit.html?', params, verify=False
    ).text
    price_list = []
    for params in get_params[0]:
        for ret_params in get_params[1]:
            get_request_1 = session.get(
                'https://en.evelop.com/b2c/pages/flight/'
                'availabilitySelectFlight.html?', params=params,
                verify=False
            ).content
            get_request_2 = session.get(
                'https://en.evelop.com/b2c/pages/flight/'
                'availabilitySelectFlight.html?', params=ret_params,
                verify=False
            ).content
            tree = html.fromstring(get_request_2)
            price = tree.xpath(
                '//*[@id="selected-routes"]/div/div/ol/li/div[1]/div[1]/div[1]'
                '/div/strong'
            )[0].text.strip().encode('latin-1').decode('utf-8')
            price_list.append(price)
    return price_list


def path_to_data(data_page, route):
    """"""

    data_path = parse_results(data_page, route)
    quote_dict = {'Outbound': None, 'Return': None}
    selected_flights = []
    for flight in data_path:
        selected_flight = []
        for data in flight:
            way = data.xpath(
                'div[@class="aerolinea"]/text()|'
                'div[@class="aerop"]/span/text()'
            )
            dep_city = re.findall(r'[A-Z]{3}', way[0])[0]
            arr_city = re.findall(r'[A-Z]{3}', way[0])[1]

            dep_time = data.xpath(
                'div[@class="salida"]/span[@class="hora"]/text()'
            )[0].strip()
            arr_time = data.xpath(
                'div[@class="llegada"]/span[@class="hora"]/text()'
            )[0].strip()

            flight_class = data.xpath(
                'div[@class="clase"]/span[@class="left clearfix clase"]'
                '/span[@class="tipo-clase"]/text()|'
                'div[@class="left clearfix clase "]/span[@class="tipo-clase"]'
                '/text()'
            )[0]

            flight = data.xpath('div[@class="radio"]/input')[0].get('onclick')
            name = re.findall(r'\(\'([A-Z0-9]+)', flight)[0]
            direction = re.findall(r'\'(\w+)\'', flight)[0]
            param_for_name_1 = re.findall(r'\'(\w+)\'', flight)[1]
            param_for_name_2 = re.findall(r'\b[A-Z0-9.+]{3,4}\b', flight)[0]

            selected_flight.append(
                {'flightId': '{0};#{1}#{2}'.format(
                    name, param_for_name_1, param_for_name_2
                ), 'direction': direction}
            )

            if data_path.index(flight) == 0:
                quote_dict['Outbound'] = dep_city, arr_city, dep_time, arr_time, flight_class
            else:
                quote_dict['Return'] = dep_city, arr_city, dep_time, arr_time, flight_class
        selected_flights.append(selected_flight)
    print(get_price(selected_flights))

    return quote_dict


def parse_results(data_page, route):
    """Get data about flights."""

    data = data_page.xpath(
        '/html/body/div[@id="content"]'
        '/div/div/form[@id="formularioValoracion"]'
        '/div/div[@class="flexcols"]/section'
        '/div[@id="tabs2"]/div/div'
    )[0]
    flights = []
    if route == 'ONE_WAY':
        result = data.xpath(
            'ol/li/div[@class="vuelo-wrap vuelo-wrap3"]'
            '/div[@class="flexcols"]/div[@class="flexcol-main datos"]/div'
        )
        flights.append(result)
    else:
        results = data.xpath(
            'div[@class="wrap-sel-custom combinado"]'
            '/div[@class="grid-cols clearfix"]/div'
        )
        for result in results:
            flights.append(
                result.xpath('div[@class="datos"]/div[position() mod 2 = 1]')
            )

    return flights


def generate_quotes(data):
    """To prepare data to print."""

    if len(data) == 0:
        quotes = None
    elif len(data) == 1:
        quotes = []
        for quote in data[0]:
            quotes.append(
                [quote[:-2],
                 str('{:.2f}'.format(quote[-1])) + ' ' + quote[-2]]
            )
    else:
        quotes = []
        for quote_ob in data[0]:
            for quote_rt in data[1]:
                quote = [
                    quote_ob[:-2], quote_rt[:-2],
                    str(
                        '{:.2f}'.format(
                            sum(
                                [quote_ob[-1], quote_rt[-1], 12]
                            )
                        )
                    ) + ' ' + quote_ob[-2]
                ]
                quotes.append(quote)

    return quotes


def scrape(search_params):
    """Get search params if necessary and return quotes."""

    if not search_params:
        search_params = manual_input(AVAILABLE_ROUTES)

    data_page = get_data_page(search_params)
    data = parse_results(data_page, search_params['flight_type'])
    quotes = generate_quotes(data)

    return quotes


def print_result(result_func):
    """Printing results."""

    flight_type_list = ['Outbound', 'Return']
    try:
        for info in result_func:
            for quote in info[:-1]:

                if type(quote) == list:
                    print(flight_type_list[info.index(quote)], '\n')
                    print('Way: {0} - {1}'.format(quote[0], quote[1]))
                    print('Date:', quote[2])
                    print('Departure time:', quote[3])
                    print('Arrival time:', quote[4])
                    print('Flight time:', quote[5])
                    print('Class:', quote[6], '\n')
            print('Total price:', info[-1])
            print('\n')
    except TypeError:
        print(
            'There is not availability enough '
            'for the selected flights. Please '
            'select another date.'
        )


if __name__ == '__main__':
    AVAILABLE_ROUTES = get_available_routes()
    QUERY_PARAMS = get_query_params_from_command_line()
    # while True:
    #     result_data = scrape(query_params)
    #     print_result(result_data)
    #     query_params = None
    #     if input(
    #         'Enter "EXIT" to close program. '
    #         'For continue press "Enter". '
    #     ).upper() == 'EXIT':
    #         break
    # search = manual_input(get_available_routes())
    a = get_data_page(QUERY_PARAMS)
    print(path_to_data(a, QUERY_PARAMS['flight_type']))
