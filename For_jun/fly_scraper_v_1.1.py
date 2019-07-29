"""Python 3.7. Scraper for www.flybulgarien.dk"""

import re
import requests

from collections import defaultdict
from lxml import html


def city():
    """
    Finding available cities
    and access to IATA code.
    For usability to user input.
    """

    connect = requests.get('http://www.flybulgarien.dk/en/').content

    tree = html.fromstring(connect)

    cities = tree.xpath(
        '/html/body/div[@id="wrapper"]'
        '/div[@id="content"]/div'
        '/form[@id="reserve-form"]'
        '/dl/dd[@class="double"][1]'
        '/select/option/text()'
    )

    city_dict = defaultdict()

    for city in cities:
        city = city.split()
        city_dict[city[0]] = re.findall(r'\w{3}', city[1])[0]
    return city_dict


def one_way_fly(dep_date, dep_city, arr_city, adults_child):
    """
    Parsing and treat data
    from site for one way flying.
    And output information about flights.
    """

    city_dict = city()

    connect = requests.get(
        'https://apps.penguin.bg/'
        'fly/quote3.aspx?ow=&lang'
        '=en&depdate={0}'
        '&aptcode1={1}&aptcode2='
        '{2}&paxcount={3}&infcount='.format(
            dep_date,
            city_dict[dep_city],
            city_dict[arr_city],
            adults_child
        )
    ).content


    tree = html.fromstring(connect)
    data = tree.xpath(
        '/html/body/form[@id="form1"]'
        '/div[@style="padding: 10px;"]'
        '/table[@id="flywiz"]/tr[1]/td/'
        'table[@id="flywiz_tblQuotes"]/tr[@id]')

    fly_list = [info.xpath('td/text()') for info in data]

    list_of_vars = []
    index_count_1 = 0
    index_count_2 = index_count_1 + 1
    while True:
        try:
            list_of_vars.append(
                fly_list[index_count_1] + fly_list[index_count_2]
            )
            index_count_1 += 2

        except IndexError:
            break

    for i in range(len(list_of_vars)):
        date = re.findall(
            r'\w{3},\s\d+\s\w+\s\d{2}', ', '.join(list_of_vars[i])
        )[0]
        departure_time = re.findall(
            r'\d{2}:\d{2}', ' '.join(list_of_vars[i])
        )
        departure_city = re.findall(
            r'\w+\s\(\w+\)', ', '.join(list_of_vars[i])
        )
        price = re.findall(
            r'\d+\.\d{2}', ', '.join(list_of_vars[i])
        )[0]
        currency = re.findall(
            r'\d+\.\d{2}\s(\w+)', ', '.join(list_of_vars[i])
        )[0]

        print('Variant number', i + 1, '\n')
        print('Date of depart: {}'.format(date))
        print('Departure city: {}'.format(departure_city[0]))
        print('Arrival city: {}'.format(departure_city[1]))
        print('Time of depart: {}'.format(departure_time[0]))
        print('Time of arrive: {}'.format(departure_time[1]))
        print('Price of flight: {0} {1}'.format(
            float(price) * adults_child, currency)
        )
        print('Number of passengers', adults_child)
        print('\n')
        return list_of_vars


def return_way_fly(dep_date, dep_city, ret_date, from_city, num_tickets):
    city_dict = city()

    connect = requests.get(
        'https://apps.penguin.bg/fly'
        '/quote3.aspx?rt=&lang=en&'
        'depdate=29.07.2019&aptcode1'
        '=BLL&rtdate=05.08.2019&aptcode2'
        '=BOJ&paxcount=1&infcount='.format(
            dep_date,
            dep_city,
            ret_date,
            from_city,
            num_tickets
        )
    ).content

    tree = html.fromstring(connect)
    data = tree.xpath(
        '/html/body/form[@id="form1"]'
        '/div[@style="padding: 10px;"]'
        '/table[@id="flywiz"]/tr[1]/td'
        '/table/tr')

    fly_info = []
    for info in data:
        fly_type = info.xpath('th/text()')
        fly = info.xpath('td/text()')
        if len(fly_type) == 1:
            fly_info.append(fly_type)
        if len(fly) > 0:
            fly_info.append(fly)
    list_of_vars = []
    while True:
        try:
            fly_info = iter(fly_info)
            list_of_vars.append(' '.join(next(fly_info)))
        except StopIteration:
            break
    info_string = ', '.join(list_of_vars)
    first_flight = re.findall(r'Going Out,\s(.+),\sComing Back', info_string)[0]
    return_flight = re.findall(r'Coming Back,\s(.+)', info_string)[0]
    first_date = re.findall(r'\w{3},\s\d+\s\w+\s\d{2}', first_flight)
    return_date = re.findall(r'\w{3},\s\d+\s\w+\s\d{2}', return_flight)
    return_time = re.findall(r'\d{2}:\d{2}', return_flight)
    return_cities = re.findall(r'\w+\s\(\w+\)', return_flight)
    price = re.findall(r'\d+\.\d{2}', return_flight)
    currency = re.findall(r'\d+\.\d{2}\s(\w+)', return_flight)
    print(first_flight)
    print(return_flight)
    # print(first_date)
    print(return_date[0])
    print(return_time)
    print(return_cities)
    print(price)
    print(currency)




if __name__ == "__main__":
    while True:
        available_cities = city()
        flight_variants = 'return'
        # flight_variants = input(
        #     'Please, choose a type of'
        #     ' flight(input "oneway" or "return"): '
        # )
        # if flight_variants == 'oneway':
        #     departure_date = input(
        #         'Please, enter a intended date'
        #         ' of flight(format enter: dd.mm.yyyy): '
        #     )
        #     departure_city = input(
        #         'Please, enter a city from '
        #         'where you wants to fly: '
        #     )
        #     arrival_city = input(
        #         'Please, enter a city where '
        #         'you want to flight: '
        #     )
        #     number_of_tickets = int(input(
        #         'Please, enter a number of tickets: ')
        #     )
        #     one_way_fly(
        #         departure_date,
        #         departure_city,
        #         arrival_city,
        #         number_of_tickets
        #     )
        #     result = one_way_fly(
        #         departure_date,
        #         departure_city,
        #         arrival_city,
        #         number_of_tickets
        #     )
        #
        #     if result == None:
        #         print('No available flights found.')
        if flight_variants == 'return':
            return_way_fly('29.07.2019', available_cities['Billund'], '05.08.2019', available_cities['Burgas'], 1)

        break
