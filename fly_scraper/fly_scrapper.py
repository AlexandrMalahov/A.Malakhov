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


def flights(
        fly_vars,
        dep_date,
        dep_city,
        arr_city,
        tickets_num
):
    """
    Finding data from flight. Data processing and output to screen.
    Function returns list information about flights.
    """

    city_dict = city()
    if fly_vars == 'oneway':
        connect = requests.get(
            'https://apps.penguin.bg/fly'
            '/quote3.aspx?ow=&lang=en&'
            'depdate={0}&aptcode1='
            '{1}&aptcode2={2}&paxcount={3}'
            '&infcount='.format(
                dep_date,
                city_dict[dep_city.capitalize()],
                city_dict[arr_city.capitalize()],
                tickets_num
            )
        ).content

        tree = html.fromstring(connect)
        data = tree.xpath(
            '/html/body/form[@id="form1"]'
            '/div[@style="padding: 10px;"]'
            '/table[@id="flywiz"]/tr/td/'
            'table/tr/td//text()'
        )

        try:
            price = '{:.2f}'.format(float(re.findall(r'\d+\.\d{2}', data[-1])[0]))
            currency = re.findall(r'\d+\.\d{2}\s(\w+)', data[-1])[0]

            # Next block of code calculates flights time
            flights_time_ow_dep = data[1].split(':')
            fligths_time_ow_arr = data[2].split(':')
            fligths_time_ow_dep = int(flights_time_ow_dep[0]) * 60 + int(flights_time_ow_dep[1])
            flights_time_ow_arr = int(fligths_time_ow_arr[0]) * 60 + int(fligths_time_ow_arr[1])
            hours = (flights_time_ow_arr - fligths_time_ow_dep) // 60
            mins = (flights_time_ow_arr - fligths_time_ow_dep) % 60

            # Outputing a result
            print('Type of flight: One way flight', '\n')
            print('Going out:', '\n')
            print('Flight date: {}'.format(data[0]))
            print('Departure city: {}'.format(data[3]))
            print('Time of flight starts: {}'.format(data[1]))
            print('Arrival city: {}'.format(data[4]))
            print('Time of ending flight: {}'.format(data[2]))
            print('Time of flight: {0} hours, {1} minutes'.format(hours, mins))
            print('Price for {0} ticket(s): {1} {2}'.format(
                tickets_num,
                '{:.2f}'.format(
                    float(price) * tickets_num
                ),
                currency
            ))
            print('\n')
        except IndexError:
            print('No available flights found.')
        return data

    elif fly_vars == 'return':
        # Enter and checking return date
        while True:
            ret_date = input(
                'Please, enter a return date'
                '(format enter: dd.mm.yyyy): '
            )
            try:
                day = int(re.findall(r'\d{2}', ret_date)[0])
                month = int(re.findall(r'\.(\d{2})\.', ret_date)[0])
                year = int(re.findall(r'\d{4}', ret_date)[0])
                if 1 <= day <= 31 and 1 <= month <= 12 and 2019 <= year:
                    break
                else:
                    print('Enter a correct date.')
                    continue
            except IndexError:
                print('Enter a correct date.')
                continue

        connect = requests.get(
            'https://apps.penguin.bg/fly/'
            'quote3.aspx?rt=&lang=en&depdate'
            '={0}&aptcode1={1}'
            '&rtdate={2}&aptcode2={3}'
            '&paxcount={4}&infcount='.format(
                dep_date,
                city_dict[dep_city.capitalize()],
                ret_date,
                city_dict[arr_city.capitalize()],
                tickets_num
            )
        ).content

        tree = html.fromstring(connect)
        data = tree.xpath(
            '/html/body/form[@id="form1"]'
            '/div[@style="padding: 10px;"]'
            '/table[@id="flywiz"]/tr/td/'
            'table/tr/td//text()'
        )

        new_data = []

        if 'No available flights found.' in data:
            for info in data:
                if info == 'No available flights found.':
                    index = data.index(info)

                    data.pop(index)
                    if index == 0:
                        return_flight = data
                        new_data.append([info])
                        new_data.append(return_flight)
                    else:
                        first_flight = data
                        new_data.append(first_flight)
                        new_data.append([info])

        else:
            len_data_list = int(len(data) / 2)
            new_data.append(data[:len_data_list])
            new_data.append(data[len_data_list:])

        first_flight_info = new_data[0]

        if first_flight_info[0] == 'No available flights found.':
            print('Going out.', '\n')
            print(first_flight_info[0])
            print('\n')
        else:
            price = '{:.2f}'.format(float(re.findall(r'\d+\.\d{2}', ''.join(first_flight_info))[0]))

            currency = re.findall(r'\d+\.\d{2}\s(\w+)', ' '.join(first_flight_info))[0]

            # Next block of code calculates flights time
            fligths_time_dep = first_flight_info[1].split(':')
            fligths_time_arr = first_flight_info[2].split(':')
            fligths_time_dep = int(fligths_time_dep[0]) * 60 + int(fligths_time_dep[1])
            fligths_time_arr = int(fligths_time_arr[0]) * 60 + int(fligths_time_arr[1])
            flights_time_hours = (fligths_time_arr - fligths_time_dep) // 60
            fligths_time_min = (fligths_time_arr - fligths_time_dep) % 60

            # Outputing a result
            print('Going out.', '\n')
            print('Departure date: {}'.format(first_flight_info[0]))
            print('Departure time: {0}, Arrival time: {1}'.format(first_flight_info[1], first_flight_info[2]))
            print('Departure city: {0}, Arrival city: {1}'.format(first_flight_info[3], first_flight_info[4]))
            print('Number of passengers: {}'.format(tickets_num))
            print('Time of flight: {0} hours, {1} minutes'.format(flights_time_hours, fligths_time_min))
            print(
                'Price for {0} ticket(s): {1} {2}'.format(
                    tickets_num, '{:.2f}'.format(
                        float(price) * tickets_num),
                    currency
                )
            )
            print('\n')

        second_flight_info = new_data[1]

        if second_flight_info[0] == 'No available flights found.':
            print('Coming_back.', '\n')
            print(second_flight_info[0])
            print('\n')
        else:

            price = '{:.2f}'.format(float(re.findall(r'\d+\.\d{2}', ' '.join(second_flight_info))[0]))

            currency = re.findall(r'\d+\.\d{2}\s(\w+)', ' '.join(second_flight_info))[0]

            # Next block of code calculates flights time
            fligths_time_dep = second_flight_info[1].split(':')
            fligths_time_arr = second_flight_info[2].split(':')
            fligths_time_dep = int(fligths_time_dep[0]) * 60 + int(fligths_time_dep[1])
            fligths_time_arr = int(fligths_time_arr[0]) * 60 + int(fligths_time_arr[1])
            flights_time_hours = (fligths_time_arr - fligths_time_dep) // 60
            fligths_time_min = (fligths_time_arr - fligths_time_dep) % 60

            # Outputing a result
            print('Coming back.', '\n')
            print('Departure date: {}'.format(second_flight_info[0]))
            print('Departure time: {0}, Arrival time: {1}'.format(second_flight_info[1], second_flight_info[2]))
            print('Departure city: {0}, Arrival city: {1}'.format(second_flight_info[3], second_flight_info[4]))
            print('Number of passengers: {}'.format(tickets_num))
            print('Time of flight: {0} hours, {1} minutes'.format(flights_time_hours, fligths_time_min))
            print(
                'Price for {0} ticket(s): {1} {2}'.format(
                    tickets_num, '{:.2f}'.format(
                        float(price) * tickets_num),
                    currency
                )
            )
            print('\n')
        return new_data


def correct_way():
    """Checking input of way type for correct."""

    while True:
        flight_variants = input(
            'Please, choose a type '
            'of flight(input "oneway" or "return"): '
        )
        if flight_variants == 'oneway' or flight_variants == 'return':
            break
        else:
            print('Enter a correct type of flight.')
    return flight_variants


def correct_date():
    """Cheking input of date for correct."""

    while True:
        departure_date = input(
            'Please, enter a intended'
            ' date of flight(format enter: dd.mm.yyyy): '
        )
        try:
            day = int(re.findall(r'\d{2}', departure_date)[0])
            month = int(re.findall(r'\.(\d{2})\.', departure_date)[0])
            year = int(re.findall(r'\d{4}', departure_date)[0])
            if 1 <= day <= 31 and 1 <= month <= 12 and 2019 <= year:
                break
            else:
                print('Enter a correct date.')
                continue
        except IndexError:
            print('Enter a correct date.')
            continue
    return departure_date



def correct_dep_city():
    """Checking for correct input cities."""

    city_dict = city()
    while True:
        departure_city = input(
            'Please, enter a city from '
            'where you wants to fly: '
        )

        if departure_city.capitalize() in city_dict:
            break
        else:
            print(
                'Enter correct cities names'
                '(Available cities: "Copenhagen",'
                '"Billund", "Plovdiv", "Burgas",'
                '"Sofia", "Varna")'
            )
            continue
    return departure_city


def correct_arr_city():
    """Checking for correct input cities."""

    city_dict = city()
    while True:
        arrival_city = input(
            'Please, enter a city where '
            'you want to flight: '
        )
        if arrival_city.capitalize() in city_dict:
            break
        else:
            print(
                'Enter correct cities names'
                '(Available cities: "Copenhagen",'
                '"Billund", "Plovdiv", "Burgas",'
                '"Sofia", "Varna")'
            )
            continue
    return arrival_city


def correct_tickets():
    """Checking number of tickets."""

    while True:
        number_of_tickets = int(
            input(
                'Please, enter a number of tickets: '
            )
        )
        if 0 < number_of_tickets < 9:
            break
        else:
            print(
                'Number of tickets must be '
                'no more than 8 for one reserve.'
            )
            continue
    return number_of_tickets


if __name__ == "__main__":
    way = correct_way()
    dep_date = correct_date()
    dep_city = correct_dep_city()
    arr_city = correct_arr_city()
    number_of_tickets = correct_tickets()
    flights(way, dep_date, dep_city, arr_city, number_of_tickets)
