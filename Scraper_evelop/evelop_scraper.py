"""Python 3.7. Parsing of the web site https://www.evelop.com/."""


import argparse
import datetime
import json
import re
import requests

from lxml import html


def check_flight_type(flight_type):
    """Check that flight type is valid."""

    try:
        flight_type = flight_type.upper()
    except AttributeError:
        return False
    if flight_type in {'ONE_WAY', 'ROUND_TRIP'}:
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
    elif arr_city not in AVAILABLE_ROUTES[dep_city]:
        print('No such routes.')
        print('Available routes: ')
        for dep_airport in AVAILABLE_ROUTES:
            print(dep_airport, 'to', AVAILABLE_ROUTES[dep_airport])
        return False
    elif dep_city == arr_city:
        print("Departure city mustn't be same arrival city.")  # with
        return False

    return True


def check_dates(*dates):
    """Check if dates are valid."""

    today = datetime.datetime.now().date()
    for date in dates:
        try:
            date = re.findall(
                r'\b(\d{2})[.-/](\d{2})[.-/](\d{4})\b', date)[0]
        except IndexError:
            print('Incorrect date.')
            return False
        except TypeError:
            print('You did not enter a date.')
            return False
        date = datetime.date(*map(int, reversed(date)))
        if not date:
            print('Incorrect date')
            return False
        if date <= today:
            print(
                'Departure date must be greater than today '
                'and return date greater than departure date.'
            )
            return False
        today = date

    return True


def check_passengers(adults, children, infants):
    """Check number of passengers."""

    try:
        adults = int(adults)
        children = int(children)
        infants = int(infants)
    except ValueError:
        print('Number of passengers must be integer number.')
        return False
    except TypeError:
        print('You did not enter number of adults, children or infants.')
        return False

    if adults <= 0 or adults > 9:
        print(
            'Number of adults must be more '
            'or equal 1 and less or equal 9.'
        )
        return False

    if children < 0 or children + adults > 9:
        print(
            'Number of children must be more or equal 0 '
            'and less or equal number of adults, and '
            'sum of number of adults and children must '
            'not be more than 9.'
        )
        return False

    if infants < 0 or infants > adults or infants > 5:
        print(
            'Number of infants must be more or equal '
            '0 and less or equal number of adults.'
        )
        return False

    return True


def get_query_params_from_command_line():
    """Parse and check arguments of command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--flight_type', help='input flight type("ONE_WAY" or "ROUND_TRIP")'
    )
    parser.add_argument(
        '-d', '--dep_city', help='input departure city(three-digit IATA code)')
    parser.add_argument(
        '-a', '--arr_city', help='input arrival city(three-digit IATA code)')
    parser.add_argument('-d_d', '--dep_date', help='input departure date')
    parser.add_argument('-r', '--ret_date', help='input return date')
    parser.add_argument('-n_a', '--num_adults', help='input number of adults')
    parser.add_argument('-n_c', '--num_child', help='input number of children')
    parser.add_argument(
        '-n_i', '--num_infants', help='input number of infants')

    args = parser.parse_args()

    if not check_flight_type(args.flight_type):
        return None

    if not check_cities(args.dep_city, args.arr_city):
        return None

    if args.flight_type.upper() == 'ONE_WAY':
        if not check_dates(args.dep_date):
            return None
        args.ret_date = args.dep_date
    else:
        if not check_dates(args.dep_date, args.ret_date):
            return None

    if not check_passengers(args.num_adults, args.num_child, args.num_infants):
        return None

    return {
        'flight_type': args.flight_type.upper(),
        'dep_city': args.dep_city.upper(),
        'arr_city': args.arr_city.upper(),
        'dep_date': args.dep_date,
        'ret_date': args.ret_date,
        'adults': args.num_adults,
        'children': args.num_child,
        'infants': args.num_infants
    }


def manual_input():
    """Get query params from manual input."""

    while True:
        flight_type = input(
            'Please, enter type of flight ("ONE_WAY" or "ROUND_TRIP"): '
        ).upper()

        if check_flight_type(flight_type):
            break

    while True:
        dep_city = input(
            'Please, enter IATA code of departure city({}): '.format(
                ', '.join(AVAILABLE_ROUTES))
        ).upper()

        arr_city = input(
            'Please, enter IATA code of arrival city({}): '.format(
                ', '.join(AVAILABLE_ROUTES[dep_city]))
        ).upper()

        if check_cities(dep_city, arr_city):
            break

    while True:
        dep_date = input('Please, enter departure date(dd/mm/yyyy): ').upper()

        if flight_type == 'ROUND_TRIP':
            ret_date = input('Please, enter return date(dd/mm/yyyy): ')
            if check_dates(dep_date, ret_date):
                break
        else:
            if check_dates(dep_date):
                ret_date = dep_date
                break

    while True:
        adults = input(
            'Please, enter a number of adults'
            '(number must be more than 0 and less or equal 9): '
        )
        children = input(
            'Please, enter a number of children (number must be more or '
            'equal than 0 and less or equal number of adults): '
        )
        infants = input(
            'Please, enter a number of infants (number must be more or '
            'equal than 0 and less or equal number of adults): '
        )

        if check_passengers(adults, children, infants):
            break

    return {
        'flight_type': flight_type,
        'dep_city': dep_city,
        'arr_city': arr_city,
        'dep_date': dep_date,
        'ret_date': ret_date,
        'adults': adults,
        'children': children,
        'infants': infants
    }


def get_available_routes():
    """Generate list of available routes."""

    response = requests.get('https://en.evelop.com/', verify=False).content

    routes_json = re.findall(r'routesWebSale = ({.+});', str(response))[0]
    routes = re.split(';', routes_json)[0]
    routes_json = json.loads(routes)

    return routes_json


def generate_request_params(search_params):
    """Generate params for get web-page with search results."""

    return {
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


def get_data_page(search_params):
    """Get html page from web-site."""

    params = generate_request_params(search_params)
    tree = html.fromstring(
        requests.post(
            'https://en.evelop.com/b2c/pages/flight/'
            'disponibilidadSubmit.html?',
            params,
            verify=False
        ).content
    )

    return tree


def parse_results(data_page, search_params):
    """Get and generate quotes of flights."""

    try:
        data = data_page.xpath(
            '/html/body/div[@id="content"]/div/div'
            '/form[@id="formularioValoracion"]/div/div[@class="flexcols"]'
            '/section/div[@id="tabs2"]/div/div'
        )[0]
    except IndexError:
        return None
    flights = []
    if search_params['flight_type'] == 'ONE_WAY':
        results = data.xpath(
            'ol/li/div[@class="vuelo-wrap vuelo-wrap3"]/div[@class="flexcols"]'
        )

        for result in results:
            flight_dict = {}
            price = result.xpath(
                'div[@class="flexcol-right acciones3 clearfix"]'
                '/div/div/strong/text()'
            )[0]

            flight_data = parse_data_div(
                result.xpath('div[@class="flexcol-main datos"]/div')[0])

            flight_data['flight_time'] = generate_flight_time(
                flight_data['dep_time'], flight_data['arr_time']) ################################################################################
            flight_data['date'] = search_params['dep_date']
            flight_dict['Outbound'] = flight_data
            flight_dict['price'] = price
            flights.append(flight_dict)

    else:
        # The result consists of two nested lists.
        # The first one contains "outbound" flights,
        # the second one contains "return" flights.
        results = data.xpath(
            'div[@class="wrap-sel-custom combinado"]'
            '/div[@class="grid-cols clearfix"]/div'
        )
        data_xpath = 'div[@class="datos"]/div[position() mod 2 = 1]' ####################################################
        # Generate flights combinations.
        for flight_ob in results[0].xpath(data_xpath):
            outbound_dict = parse_data_div(flight_ob)
            for flight_ib in results[1].xpath(data_xpath):

                return_dict = parse_data_div(flight_ib)

                flight_info = {
                    'Outbound': outbound_dict, 'Return': return_dict}

                flights.append(flight_info)

                outbound_dict['flight_time'] = generate_flight_time(
                    outbound_dict['dep_time'], outbound_dict['arr_time']
                )
                return_dict['flight_time'] = generate_flight_time(
                    return_dict['dep_time'], return_dict['arr_time']
                )

                outbound_dict['date'] = search_params['dep_date']
                return_dict['date'] = search_params['ret_date']

                search_params_for_ow = flight_ob.xpath(
                    'div[@class="radio"]/input')[0].get('onclick')
                search_params_for_rt = flight_ib.xpath(
                    'div[@class="radio"]/input')[0].get('onclick')
                flight_info['price'] = get_price(
                    search_params_for_ow, search_params_for_rt,
                    generate_request_params(search_params)
                )

    return flights


def parse_data_div(data_div):
    """Parse div elements with data from web page."""

    route = data_div.xpath(
        'div[@class="aerolinea"]/text()|div[@class="aerop"]/span/text()'
    )[0]
    dep_city, arr_city = route.replace(
        ' ', '').replace('\n', '').replace('\t', '').split('-')
    dep_time = data_div.xpath(
        'div[@class="salida"]/span[@class="hora"]/text()')[0].strip()
    arr_time = data_div.xpath(
        'div[@class="llegada"]/span[@class="hora"]/text()')[0].strip()
    cabin_class = data_div.xpath(
        'div[@class="clase"]/span[@class="left clearfix clase"]'
        '/span[@class="tipo-clase"]/text()|'
        'div[@class="left clearfix clase "]/span[@class="tipo-clase"]/text()'
    )[0]

    return {
        'dep_city': dep_city,
        'arr_city': arr_city,
        'dep_time': dep_time,
        'arr_time': arr_time,
        'cabin_class': cabin_class
    }


def generate_flight_time(dep_time, arr_time):
    """Calculate flight time."""

    dep_time = dep_time.split(':')
    arr_time = arr_time.split(':')
    dep_time = datetime.timedelta(
        hours=float(dep_time[0]), minutes=float(dep_time[1]))
    arr_time = datetime.timedelta(
        hours=float(arr_time[0]), minutes=float(arr_time[1]))

    return re.findall(r'\w{1,2}:\w{2}', str(arr_time - dep_time))[0]


def get_price(param_outbound, param_inbound, params_post):
    """Get price for round trip way."""

    session = requests.session()

    session.post(
        'https://en.evelop.com/b2c'
        '/pages/flight/disponibili'
        'dadSubmit.html?',
        params_post,
        verify=False
    )

    for param in param_outbound, param_inbound:

        #  Find the necessary data for query parameters.
        extra_get_param_data = param.split('(')[1].replace("'", '').replace(
            '\n', '').replace(r'\s+', '').split(',')

        #  Substitute the needed data into the request
        extra_get_param = '#'.join(
            extra_get_param_data[i].strip() for i in (0, 3, 4))

        #  Route type, which was found in
        #  "extra_get_param_data" for query params.
        direction = extra_get_param_data[1]
        get_request_for_round_trip = session.get(
            'https://en.evelop.com/b2c/pages/flight/'
            'availabilitySelectFlight.html?',
            params={'flightId': extra_get_param, 'direction': direction},
            verify=False
        ).content
    tree = html.fromstring(get_request_for_round_trip)

    price = tree.xpath(
        '/html/body/div[@id="tabs2"]/div/div/div[@id="selected-routes"]/div'
        '/div/ol/li/div[@class="vuelo-wrap"]/div[@class="flexcols"]'
        '/div[@class="flexcol-right acciones"]/div/strong/text()'
    )[0].strip().encode('latin-1').decode('utf-8')

    return price


def scrape(search_params):
    """Get search params if necessary and return quotes."""

    if not search_params:
        search_params = manual_input()

    data_page = get_data_page(search_params)
    data = parse_results(data_page, search_params)

    return data


def print_result(result_func):
    """Print results."""

    if result_func is None:
        print(
            'There is not availability enough for the '
            'selected flights. Please select another date.'
        )
    else:
        for quote in result_func:
            for key in quote:
                value = quote.get(key)
                if isinstance(value, dict):
                    print(key, '\n')
                    print(
                        'Route: {0} - {1}'.format(
                            value['dep_city'], value['arr_city']
                        )
                    )
                    print('Date:', value['date'])
                    print('Departure time:', value['dep_time'])
                    print('Arrival time:', value['arr_time'])
                    print('Flight time:', value['flight_time'])
                    print('Class:', value['cabin_class'], '\n')
            print('Price:', quote['price'])
            print('-------------------------------------------')


if __name__ == '__main__':
    AVAILABLE_ROUTES = get_available_routes()
    QUERY_PARAMS = get_query_params_from_command_line()
    while True:
        RESULT_DATA = scrape(QUERY_PARAMS)
        print_result(RESULT_DATA)
        QUERY_PARAMS = None
        if input(
                'Enter "EXIT" to close program. For continue press "Enter". '
        ).upper() == 'EXIT':
            break
