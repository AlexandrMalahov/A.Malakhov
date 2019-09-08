import argparse
import datetime
import json
import evelop_scraper
import re
import requests
import os
import sqlite3


def manual_input():

    while True:
        dep_city = input('Enter departure city: ').upper()
        arr_city = input('Enter arrival city: ').upper()
        if evelop_scraper.check_cities(dep_city, arr_city,
                                       evelop_scraper.get_available_routes()):
            break
    return dep_city, arr_city


def input_query_params():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dep_city', help='Input departure city.')
    parser.add_argument('-a', '--arr_city', help='Input arrival city.')
    args = parser.parse_args()
    try:
        dep_city = args.dep_city.upper()
        arr_city = args.arr_city.upper()
    except AttributeError:
        return None

    if not evelop_scraper.check_cities(dep_city, arr_city,
                                       evelop_scraper.get_available_routes()):
        return None

    return dep_city, arr_city


def finding_available_dates():
    """"""

    response = requests.get('https://en.evelop.com/').content
    dates = re.findall(r'routesWebSale = ({.+});', str(response))[0]
    dates = re.split(';', dates)[1]
    dates = re.findall(r'\[(.+)]', dates)[0]
    dates = re.sub(r'}(,){', ' ', dates).split()
    list_of_dicts = []
    for flight in dates:
        flight = re.search(r'[^{](.+)[^}]', flight).group()
        list_of_dicts.append(json.loads('{' + flight + '}'))

    return list_of_dicts


def find_info_on_query(search_params):
    """"""

    dep_city = search_params[0]
    arr_city = search_params[1]
    dict_with_dates = finding_available_dates()
    dep_day_list = ['-', '-', '-', '-', '-', '-', '-']
    for flight in dict_with_dates:
        if dep_city == flight['origin'] and arr_city == flight['destination']:
            for date in flight['dates']:
                date = datetime.datetime.strptime(date, '%d-%m-%Y')
                day = datetime.datetime.weekday(date)
                dep_day_list[day] = '+'
            flight_list = [
                flight['origin'],
                flight['destination'],
                ''.join(dep_day_list)
            ]

            return flight_list


def create_table():

    conn = sqlite3.connect('fly_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE Flight_schedule(ID INTEGER PRIMARY '
        'KEY AUTOINCREMENT, Dep_airport, Arr_airport, flight_schedule)'
    )


def update_table(find_info):
    """"""

    conn = sqlite3.connect('fly_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Flight_schedule(Dep_airport, Arr_airport, '
        'flight_schedule) VALUES (?, ?, ?)', find_info
    )

    conn.commit()


def select_data_table(search_params):

    dep_city = search_params[0]
    arr_city = search_params[1]

    conn = sqlite3.connect('fly_database.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM Flight_schedule WHERE Dep_airport=? AND Arr_airport=?"
    cursor.execute(sql, [dep_city, arr_city])
    result = cursor.fetchall()

    return result


def print_result(func):
    print('Departure city:', func[0])
    print('Arrival city:', func[1])
    print('Flight schedule:', func[2])


def start_program(search_params):

    try:
        select = select_data_table(search_params)
    except sqlite3.OperationalError:
        create_table()
        select = select_data_table(search_params)

    if not select:
        info = find_info_on_query(search_params)
        update_table(info)
        print('Data not found in table. Data from web-site:', '\n')
        print_result(info)
        print('Table was updated.')
    else:
        print('Data from table:', '\n')
        print_result(select[0][1:])


if __name__ == '__main__':
    params = input_query_params()
    if not params:
        search_params = manual_input()
    while True:
        if not os.path.isfile('fly_database.db'):
            create_table()
        start_program(params)
        params = None
        if input(
                'For exit enter "exit". For exit press "Enter".'
        ).upper() == 'EXIT':
            break


