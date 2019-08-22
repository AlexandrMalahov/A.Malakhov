"""For scraper. Timedelta function(only for 'ONE_WAY')."""

import datetime
import re


def time_difference(data_func):
    data = data_func

    for d in data:
        dep_time = re.findall(r'\d{1,2}:\d{2}', ' '.join(d))[0].split(':')
        dep_hour = float(dep_time[0])
        dep_minutes = float(dep_time[1])
        arr_time = re.findall(r'\d{1,2}:\d{2}', ' '.join(d))[1].split(':')
        arr_hour = float(arr_time[0])
        arr_minutes = float(arr_time[1])
        flight_time_1 = datetime.timedelta(hours=dep_hour, minutes=dep_minutes)
        flight_time_2 = datetime.timedelta(hours=arr_hour, minutes=arr_minutes)
        return flight_time_2 - flight_time_1
