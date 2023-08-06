import requests
import pandas as pd
import time
import datetime


def get_buses_data(frequence, timerange, path): # both in min
    """
    Download Autobusy i tranwaje online from Otwarte dane po warszawsku
    :param frequence: frequency of requesting data, in minutes
    :param timerange: duration of collecting data, in minutes
    :param path: path to save collected data
    """
    start_datetime = datetime.datetime.now()
    print(start_datetime, "Dowloading bus data...")
    span_added = datetime.timedelta(minutes=timerange)
    end_date_and_time = start_datetime + span_added

    while datetime.datetime.now() <= end_date_and_time:
        try:
            response = requests.get(
            "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e927d-4ad3-9500-4ab9e55deb59&apikey=a0069121-f1a7-4b53-9c37-855f3e75748e&type=1"
            )
            df = pd.json_normalize(response.json(), 'result')
            df.to_csv(f'{path}.csv', mode='w+', header=False, index=False)
            time.sleep(frequence * 60)
        except TypeError:
            pass
    print(datetime.datetime.now(), "Completed downloading bus data")


def reformat_json(raw_json):
    """
    Reformat api response to list of python dictionaries
    :param raw_json: response from the api
    :param reformatted: list of python dictionaries
    """
    reformatted = []
    for dic in raw_json:
        values = dic['values']
        details_dict = {}
        for value in values:
            details_dict[value['key']] = value['value']
        reformatted.append(details_dict)
    return reformatted


def remove_stops_with_nulls(reformatted):
    """
    Remove stops with null coordinates
    :param reformatted: reformatted api reponse
    :return: nulls_removed: only stops with not null coordinates
    """
    nulls_removed = []
    for dic in reformatted:
        if dic['szer_geo'] != 'null' or dic['dlug_geo'] != 'null':
            nulls_removed.append(dic)
    return nulls_removed


def get_stops_data(path):
    """
    Download Współrzędne przystanków from Otwarte dane po warszawsku
    :param path: path to save collected data
    """
    response = requests.get(
        'https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=a0069121-f1a7-4b53-9c37-855f3e75748e'
    )

    result = response.json()['result']
    reformatted_result = reformat_json(result)
    nulls_removed_result = remove_stops_with_nulls(reformatted_result)
    df = pd.DataFrame(nulls_removed_result)
    print(df)
    df.to_csv(f'{path}.csv', mode='w', header=False, index=False)
    print(datetime.datetime.now(), "Completed downloading stops data")


def collect_bus_and_stops_data(frequence, timerange, bus_data_path, stops_data_path):
    get_buses_data(frequence, timerange, bus_data_path)
    get_stops_data(stops_data_path)


def get_timetable_for_line(stop_id, stop_nr, line):
    """
    Download Rozkłady jazdy ZTM from Otwarte dane po warszawsku
    :param stop_id: id of stop
    :param stop_nr: nr of stop
    :param line: bus line
    """
    stop_nr = str(stop_nr)
    if len(stop_nr) == 1:
        stop_nr = '0' + stop_nr

    parameters = {
        "busstopId": str(stop_id),
        "busstopNr": stop_nr,
        "line": str(line)
    }
    response = requests.get('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&apikey=a0069121-f1a7-4b53-9c37-855f3e75748e',
                            params=parameters
                            )

    result = response.json()['result']
    reformatted_result = reformat_json(result)
    return reformatted_result
