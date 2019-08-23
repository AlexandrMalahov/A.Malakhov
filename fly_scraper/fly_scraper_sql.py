import datetime
import fly_scraper_orbest
import re
import requests
import sys
import sqlite3

from lxml import html


def checking_day(dep_date_func, ret_date_func):
    dep_day_list = ['-', '-', '-', '-', '-', '-', '-']
    date = datetime.datetime.strptime(dep_date_func, '%d/%m/%Y')
    day = datetime.datetime.weekday(date)
    dep_day_list[day] = '+'

    ret_day_list = ['-', '-', '-', '-', '-', '-', '-']
    date = datetime.datetime.strptime(ret_date_func, '%d/%m/%Y')
    day = datetime.datetime.weekday(date)
    ret_day_list[day] = '+'
    return ''.join(dep_day_list), ''.join(ret_day_list)


def create_table(params_func, data_func):
    schedule = checking_day(params_func[3], params_func[4])
    way = params_func[0]
    data = data_func
    conn = sqlite3.connect('fly_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            'CREATE TABLE Flights'
            '(ID INTEGER PRIMARY KEY AUTOINCREMENT, '
            'DEPART_DATE, DEPART_IATA, ARRIVE_IATA, PRICE, CLASS, FLIGHT_SCHEDULE)'
        )
    except sqlite3.OperationalError:
        pass

    if way == 'ONE_WAY':
        flights = []
        for info in data:
            dep_city = re.findall(r'(\w+)\s', info[3])[0]
            arr_city = re.findall(r'\s(\w+)', info[3])[0]
            flights.append([params_func[3], dep_city, arr_city, info[0], info[9], schedule[0]])

        cursor.executemany(
            'INSERT INTO Flights (DEPART_DATE, DEPART_IATA, '
            'ARRIVE_IATA, PRICE, CLASS, FLIGHT_SCHEDULE) '
            'VALUES (?, ?, ?, ?, ?, ?)', flights
        )
        conn.commit()
    elif way == 'ROUND_TRIP':
        data = data_func
        dep_flights = []
        for info in data[0]:
            dep_city = re.findall(r'\w+', ' '.join(info))[0]
            arr_city = re.findall(r'\w+', ' '.join(info))[1]
            dep_flights.append([params_func[3], dep_city, arr_city, info[3], info[2], schedule[0]])
        ret_flights = []
        for info in data[1]:
            dep_city = re.findall(r'\w+', ' '.join(info))[0]
            arr_city = re.findall(r'\w+', ' '.join(info))[1]
            ret_flights.append([params_func[4], dep_city, arr_city, info[3], info[2], schedule[1]])
        cursor.executemany(
            'INSERT INTO Flights (DEPART_DATE, DEPART_IATA, '
            'ARRIVE_IATA, PRICE, CLASS, FLIGHT_SCHEDULE) '
            'VALUES (?, ?, ?, ?, ?, ?)', dep_flights
        )
        cursor.executemany(
            'INSERT INTO Flights (DEPART_DATE, DEPART_IATA, '
            'ARRIVE_IATA, PRICE, CLASS, FLIGHT_SCHEDULE) '
            'VALUES (?, ?, ?, ?, ?, ?)', ret_flights
        )

        conn.commit()
    if data == list() or data == [[], []]:
        print('Data not found.')
    else:
        print('Data was added to table')


def select_data_table():
    dep_date = input('Enter a date to choose available flights: ')
    conn = sqlite3.connect('fly_database.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM Flights WHERE DEPART_DATE=?"

    cursor.execute(sql, [dep_date])
    result = cursor.fetchall()
    for i, _ in enumerate(result):
        print('Date:', result[i][1])
        print('Way: {}-{}'.format(result[i][2], result[i][3]))
        print('Class:', result[i][5])
        print('Price:', result[i][4])
        print('\n')

    return result


if __name__ == "__main__":
    while True:
        try:
            select = select_data_table()
            if select == list():
                print('Data not found.')
        except sqlite3.OperationalError:
            parameters = fly_scraper_orbest.manual_input()
            connection = fly_scraper_orbest.connection(parameters)
            data_flights = fly_scraper_orbest.scrape(connection, parameters)
            create_table(parameters, data_flights)
        finally:
            escape = input('For exit press "q". For continue press any key. ')
            if escape.upper() == 'Q':
                break
