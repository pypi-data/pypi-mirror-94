import pandas as pd

def load_data(path):
    """
    Load csv data
    :param path: path to csv data
    :return: dataframe
    """
    data = pd.read_csv(path)
    return data


# Analysis of punctuality
def mean_time_difference(bus_data_with_punctuality_path):
    """
    Calculate mean time difference in minutes between timetible arrival and actual bus arrival
    :param bus_data_with_punctuality_path: path to file containing bus data with punctuality
    :return: mean time difference in minutes
    """
    bus_data_with_punctuality_df = load_data(bus_data_with_punctuality_path)
    mean_time_diff = bus_data_with_punctuality_df['TimeDiff'].mean()
    mean_time_diff = round(mean_time_diff, 2)
    return mean_time_diff


def max_time_difference(bus_data_with_punctuality_path):
    """
    Find bus with maximal time difference in minutes between timetible arrival and actual bus arrival
    :param bus_data_with_punctuality_path: path to file containing bus data with punctuality
    :return: information about bus which has maximal time difference in minutes
    """
    bus_data_with_punctuality_df = load_data(bus_data_with_punctuality_path)
    max_time_diff_ind = bus_data_with_punctuality_df['TimeDiff'].idxmax() # index with highest vale in column
    max_time_diff_bus = bus_data_with_punctuality_df.loc[[max_time_diff_ind]]
    return max_time_diff_bus


def find_buses_exceeding_speed_threshold(buses_velocity_path, speed_threshold):
    """
    Find buses which exceeded given speed threshold
    :param buses_velocity_path: path to file containing bus data velocity
    :param speed_threshold: int, speed threshold in kmph
    :return: informations about buses exceeding speed threshold in kmph
    """
    buses_velocity_df = load_data(buses_velocity_path)
    buses_exceeding_speed = buses_velocity_df.loc[buses_velocity_df['Velocity'] > int(speed_threshold)] # to be sure int
    return buses_exceeding_speed
