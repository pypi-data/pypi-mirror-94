import datetime
import re
import sys
import pandas as pd
from geopy import distance
from wawpybus.collect import get_timetable_for_line


def load_bus_data(path):
    """
    Load file with bus data
    :param path: path to bus data file
    :return: dataframe
    """
    data = pd.read_csv(f'{path}', names=['Line', 'Lon', 'VehicleNumber', 'Datetime', 'Lat', 'Brigade'])
    data = data.sort_values(by=['Line', 'Brigade'], ignore_index=True)
    data['VehicleCoords'] = list(zip(data.Lat, data.Lon))
    return data


def load_stops_data(path):
    """
    Load file with stops data
    :param path: path to stops data file
    :return: dataframe
    """
    data = pd.read_csv(path,
                       names=['StopID', 'StopNumber', 'StopName', 'StreetID', 'Lat', 'Lon', 'Direction', 'ValidFrom'])
    data = data.sort_values(by=['StopID', 'StopNumber'], ignore_index=True)
    data['StopCoords'] = list(zip(data.Lat, data.Lon))
    return data


def process_measurement(measurement, measurements_df, stops_data):
    vehicle_coords = measurement['VehicleCoords']
    time = measurement['Datetime'].split()[1]  # separate date and time and select time
    min_dist = sys.maxsize
    nearest_stop = None
    for ind, stop in stops_data.iterrows():
        stop_coords = stop['StopCoords']
        dist = distance.great_circle(vehicle_coords, stop_coords).m
        if dist < min_dist:
            min_dist = dist
            nearest_stop = stop
    measurement_dict = {'VehicleNumber': measurement['VehicleNumber'], 'VehicleCoords': measurement['VehicleCoords'],
                        'Line': measurement['Line'], 'Time': time, 'StopID': nearest_stop['StopID'],
                        'StopNumber': nearest_stop['StopNumber'], 'StopName': nearest_stop['StopName'],
                        'Dist': round(min_dist, 2)}
    keys_values = measurement_dict.items()
    measurement_dict = {key: str(value) for key, value in keys_values}
    measurements_df = measurements_df.append(measurement_dict, ignore_index=True)
    return measurements_df


def find_closest_stops(bus_data_path, stops_data_path, bus_data_with_nearest_stops_path, lines: list = None):
    """
    Find stops closest to given bus position by coordinates
    :param bus_data_path: path to bus data file
    :param stops_data_path: path to stops data file
    :param bus_data_with_nearest_stops_path: path to output file
    :param lines: list of bus line to analyse, if not given analyse all bus lines included in bus data
    """
    stops_data = load_stops_data(stops_data_path)
    bus_data = load_bus_data(bus_data_path)

    if lines is None:
        lines_l = bus_data.Line.unique()  # if parameter lines is not given check all lines
    else:
        lines_l = lines
    bus_lines = bus_data.loc[bus_data['Line'].isin(lines_l)]  # bus_lines is a subset of bus_data

    bus_data_with_nearest_stops_df = pd.DataFrame()
    for ind, measurement in bus_lines.iterrows():
        bus_data_with_nearest_stops_df = process_measurement(measurement, bus_data_with_nearest_stops_df, stops_data)

    bus_data_with_nearest_stops_df = bus_data_with_nearest_stops_df.sort_values(by=['VehicleNumber', 'Time'],
                                                                                ignore_index=True)
    bus_data_with_nearest_stops_df.to_csv(f'{bus_data_with_nearest_stops_path}.csv', header=True, index=False)


def process_timetable_item(measurement, minimal_diff, nearest_time_from_timetable, timetable_item):
    timetable_item_time = re.sub('^(24)', '00', timetable_item['czas'])  # in data h 00 was written as 24
    timetable_dtobj = datetime.datetime.strptime(timetable_item_time, '%H:%M:%S')
    time_dtobj = datetime.datetime.strptime(measurement['Time'], '%H:%M:%S')
    if timetable_dtobj > time_dtobj:
        diff = timetable_dtobj - time_dtobj
    else:
        diff = time_dtobj - timetable_dtobj
    diff = diff.seconds / 60
    if diff < minimal_diff:
        minimal_diff = diff  # in min
        nearest_time_from_timetable = timetable_dtobj
    return minimal_diff, nearest_time_from_timetable


def check_punctuality(bus_data_with_nearest_stops_path, bus_data_with_punctuality_path):
    """
    Calculate difference between bus time arrival at stop and time given in timetable
    :param bus_data_with_nearest_stops_path: path to bus data with nearest stops file
    :param bus_data_with_punctuality_path: path to output data
    """
    measurements = pd.read_csv(bus_data_with_nearest_stops_path)

    bus_data_with_stops_df = pd.DataFrame()
    for ind, measurement in measurements.iterrows():
        timetable = get_timetable_for_line(measurement['StopID'], measurement['StopNumber'], measurement['Line'])

        if timetable:  # means bus stops at this stop
            minimal_diff = sys.maxsize
            nearest_time_from_timetable = None

            for timetable_item in timetable:
                minimal_diff, nearest_time_from_timetable = process_timetable_item(measurement, minimal_diff,
                                                                                   nearest_time_from_timetable,
                                                                                   timetable_item)

            bus_data_with_stops = {'TimeDiff': round(minimal_diff, 2), 'VehicleNumber': measurement['VehicleNumber'],
                                   'Line': measurement['Line'], 'Direction': timetable_item['kierunek'],
                                   'StopID': measurement['StopID'], 'StopNumber': measurement['StopNumber'],
                                   'Time': measurement['Time'], 'StopName': measurement['StopName'],
                                   'NearestTimeFromTimetable': nearest_time_from_timetable}
            keys_values = bus_data_with_stops.items()
            bus_data_with_stops = {key: str(value) for key, value in keys_values}
            bus_data_with_stops_df = bus_data_with_stops_df.append(bus_data_with_stops, ignore_index=True)

    bus_data_with_stops_df.to_csv(f'{bus_data_with_punctuality_path}.csv', header=True, index=False)


def check_if_exceeded_speed(bus_data_with_nearest_stops_path, buses_velocity_path):
    """
    Calculate bus speed between consecutive positions in kmph
    :param bus_data_with_nearest_stops_path: path to bus data with nearest stops file
    :param buses_velocity_path: path to bud velocity data file
    """
    bus_data_with_nearest_stops = pd.read_csv(bus_data_with_nearest_stops_path)
    vehicles = bus_data_with_nearest_stops.VehicleNumber.unique()

    buses_velocity_df = pd.DataFrame()
    for vehicle in vehicles:
        vehicle_measurements = bus_data_with_nearest_stops[bus_data_with_nearest_stops.VehicleNumber == vehicle]
        previous = vehicle_measurements.iloc[0]
        for ind, measurement in vehicle_measurements.iterrows():
            if ind == 0:
                continue
            current = measurement

            dist = distance.great_circle(eval(previous['VehicleCoords']), eval(current['VehicleCoords'])).km

            previous_dtobj = datetime.datetime.strptime(previous['Time'], '%H:%M:%S')
            current_dtobj = datetime.datetime.strptime(current['Time'], '%H:%M:%S')

            diff = current_dtobj - previous_dtobj
            diff = diff.seconds / 3600  # to obtain an hour

            velocity = dist / diff if diff != 0 else dist
            bus_velocity = {'VehicleNumber': measurement['VehicleNumber'], 'Line': measurement['Line'],
                            'EndPosition': current['VehicleCoords'], 'StartPosition': previous['VehicleCoords'],
                            'EndTime': current['Time'], 'StartTime': previous['Time'],
                            'EndNearestStopName': current['StopName'], 'StartNearestStopName': previous['StopName'],
                            'EndNearestStopNr': current['StopNumber'], 'StartNearestStopNr': previous['StopNumber'],
                            'Velocity': round(velocity, 2)}
            keys_values = bus_velocity.items()
            bus_velocity = {key: str(value) for key, value in keys_values}
            buses_velocity_df = buses_velocity_df.append(bus_velocity, ignore_index=True)

            previous = current

    buses_velocity_df.to_csv(f'{buses_velocity_path}.csv', header=True, index=False)
