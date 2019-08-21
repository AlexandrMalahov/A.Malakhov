import datetime
import new_fly_scraper
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


def create_table(type_way, data_func):
    schedule = checking_day(departure_date, return_date)
    way = type_way
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
            flights.append([departure_date, dep_city, arr_city, info[0], info[9], schedule[0]])


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
            dep_flights.append([departure_date, dep_city, arr_city, info[3], info[2], schedule[0]])
        ret_flights = []
        for info in data[1]:
            dep_city = re.findall(r'\w+', ' '.join(info))[0]
            arr_city = re.findall(r'\w+', ' '.join(info))[1]
            ret_flights.append([return_date, dep_city, arr_city, info[3], info[2], schedule[1]])
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
    print('Data was added to table')


def select_data_table():
    dep_date = departure_date
    conn = sqlite3.connect('fly_database.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM Flights WHERE DEPART_DATE=?"
    cursor.execute(sql, [dep_date])
    result = cursor.fetchall()
    return result





if __name__ == "__main__":
    counter = 0
    way_type = new_fly_scraper.correct_way(counter)
    departure_city = new_fly_scraper.correct_arr_city(counter)
    arrival_city = new_fly_scraper.correct_arr_city(counter)
    departure_date = new_fly_scraper.correct_dep_date(counter)
    return_date = new_fly_scraper.correct_ret_date(way_type, departure_date, counter)
    passengers_num = new_fly_scraper.correct_passengers(way_type, counter)
    # way_type = 'ROUND_TRIP'
    # departure_city = 'LIS'
    # arrival_city = 'CUN'
    # departure_date = '27/08/2019'
    # return_date = '22/09/2019'
    # passengers_num = (1, 0, 0)
    connection = new_fly_scraper.connection(
        way_type,
        departure_city,
        arrival_city,
        departure_date,
        return_date,
        passengers_num
    )

    data_flights = new_fly_scraper.fly_data(way_type, connection)
    select = select_data_table()
    if select == list():
        create_table(way_type, data_flights)
    else:
        print(select_data_table())


