import urllib.request
import numpy as np
import ast
import pandas as pd
import time
import geopy.distance
import os
import functools
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def load(api_key):
    """
    Loads the data from https://api.um.warszawa.pl/. One must provide their personal api key to get the data.
    :param api_key: personal api key.
    :return: pandas.DataFrame with columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    """
    url = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59&apikey={}&type=1'.format(str(api_key))
    try:
        with urllib.request.urlopen(url) as url2:
            s = str(url2.read())
        s = s.split('},')
        for i in range(len(s)):
            if not s[i].startswith('{'):
                s[i] = s[i][s[i].find('[{')+1:]
            if '}]}' not in s[i]:
                s[i] = s[i]+'}'
            else:
                s[i] = s[i][:s[i].rfind('}')-1]
        for i in range(len(s)):
            d = ast.literal_eval(s[i])
            s2 = pd.Series(d).T
            if i == 0:
                data = s2.to_frame().T
            else:
                data = pd.concat([data, s2.to_frame().T])
        data["Time"] = pd.to_datetime(data["Time"])
        data["Lon"] = pd.to_numeric(data["Lon"])
        data["Lat"] = pd.to_numeric(data["Lat"])
        data["Time"] = pd.to_datetime(data["Time"], format="%Y-%m-%d %H:%M:%S")
        return data
    except SyntaxError:
        print("Api key is not correct!")


def collect_data(how_many, period, api_key):
    """
    Collects data from https://api.um.warszawa.pl/. One must provide their personal api key to get the data.
    :param how_many: how many times should we download the data (numeric)
    :param period: how often should we download the data (timedelta)
    :param api_key: personal api key.
    :return: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes has columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    """
    dataset = []
    for i in range(how_many):
        print("Downloading "+str(i)+". dataframe, please wait...")
        now = time.time()
        dataset.append(load(api_key))
        now2 = time.time()
        if i < how_many-1:
            time.sleep(period-(now2-now))
    return dataset


def save_data_to_files(dataset, name_of_files):
    """
    Saves pandas.DataFrames from a list of dataframes to files.
    :param dataset: List of pandas.DataFrames.
    :param name_of_files: name for files. Each file will have name name_of_file_i.txt, where i is a natural number.
    :return: None
    """
    dir_name = "data"
    path = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(len(dataset)):
        with open(os.getcwd()+'/'+dir_name+"/"+name_of_files+"_{}.txt".format(str(i)), "w") as file:
            np.savetxt(file, dataset[i].values, delimiter='\t', fmt='%s')


def load_from_files(directory, name_of_files):
    """
    Loads data from files starting with the word name_of_files. Each file should be tab-separated and contain columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade" and no headers.
    :param directory: Directory containing files.
    :param name_of_files: name of files: each file with name name_of_files_i.txt, where i is a natural number, will be loaded.
    :return: list of dataframes with data from input files.
    """
    list_of_dataframes = []
    count = len([f for f in os.listdir(directory) if f.startswith(name_of_files) and os.path.isfile(os.path.join(directory, f))])
    for i in range(count):
        with open(directory+"/"+name_of_files+"_{}.txt".format(str(i)), "r") as f:
            df = pd.read_csv(f, delimiter="\t", names=["Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade"])
        df["Lon"] = pd.to_numeric(df["Lon"])
        df["Lat"] = pd.to_numeric(df["Lat"])
        df["Time"] = pd.to_datetime(df["Time"], format="%Y-%m-%d %H:%M:%S")
        list_of_dataframes.append(df)
    return list_of_dataframes

def distance(dataset, since, until):
    """

    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param since: index of list (dataset) from which we start measuring distance covered.
    :param until: index of list (dataset) at which we finish measuring distance covered.
    :return: dataframe containing two columns: VehicleNumber, Distance. Distance means distance covered between measurements in "until-moment" and "since-moment".
    """
    now = dataset[until]
    then = dataset[since]
    now = now.rename(columns={"Lon": "Lon_now", "Lat": "Lat_now", "Time": "Time_now"})
    then = then.rename(columns={"Lon": "Lon_then", "Lat": "Lat_then", "Time": "Time_then"})
    merged = pd.merge(now, then, on=["Lines", "VehicleNumber", "Brigade"], how="inner")
    lat_now = merged["Lat_now"].tolist()
    lat_then = merged["Lat_then"].tolist()
    lon_now = merged["Lon_now"].tolist()
    lon_then = merged["Lon_then"].tolist()
    list_of_tuples_now = list(zip(lat_now, lon_now))
    list_of_tuples_then = list(zip(lat_then, lon_then))
    dist = list(map(geopy.distance.geodesic, list_of_tuples_now, list_of_tuples_then))
    dist = list(map(geopy.distance.geodesic.km.fget, dist))
    merged["Distance"] = pd.Series(dist)
    result = merged[["VehicleNumber", "Distance"]]
    return result


def time_difference(dataset, since, until):
    """
    For the given dataset returns dataframe with time differences between measurements of buses' locations.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param since: index of list (dataset) from which we start calculating time difference.
    :param until: index of list (dataset) at which we finish calculating time difference.
    :return: dataframe containing two columns: VehicleNumber and Time_difference. Time_difference means the difference between measurements in "until-moment" and "since-moment".
    """
    now = dataset[until]
    then = dataset[since]
    now = now.rename(columns={"Lon": "Lon_now", "Lat": "Lat_now", "Time": "Time_now"})
    then = then.rename(columns={"Lon": "Lon_then", "Lat": "Lat_then", "Time": "Time_then"})
    merged = pd.merge(now, then, on=["Lines", "VehicleNumber", "Brigade"], how="inner")
    merged["Time_difference"] = merged["Time_now"] - merged["Time_then"]
    merged["Time_difference"] = merged["Time_difference"].dt.total_seconds()
    merged["Time_difference"] = pd.to_numeric(merged["Time_difference"])
    result = merged[["VehicleNumber", "Time_difference"]]
    return result


def inst_velocity(dataset, since, until):
    """
    Calculating instantaneous velocity since some moment of time until another moment of time. Velocity is computed as distance change divided by time change.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param since: index of list(dataset). It corresponds to the moment of time to start measuring velocity.
    :param until: index of list(dataset). It correspons to the moment of time to end measuring velocity.
    :return: dataframe containing two columns: VehicleNumber and Velocity.
    """
    dist = distance(dataset, since, until)
    t_diff = time_difference(dataset, since, until)
    merged = pd.merge(dist, t_diff, on=["VehicleNumber"], how="inner")
    merged["Velocity"] = np.NaN
    updated = (merged["Time_difference"] != 0)
    merged["Velocity"][updated] = 3600 * (merged["Distance"][updated]/merged["Time_difference"][updated])
    result = merged[["VehicleNumber", "Velocity"]]
    return result


def exceed_50(dataset, since, until):
    """
    For the given dataset returns rows with buses that exceeded 50 km/h between since-th moment of time and until-th moment of time.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param since: index of list(dataset) from which we start calculating velocity (see: help(inst_velocity))
    :param until: index of list(dataset) at which we finish calculating velocity (see: help(inst_velocity))
    :return: dataframe containing rows with data for buses that exceeded 50 km/h.
    """
    vel = inst_velocity(dataset, since, until)
    result = pd.merge(dataset[since], vel, on=["VehicleNumber"], how="inner")
    return result[result["Velocity"] > 50]


def all_exceeding_50(dataset):
    """
    For the given dataset returns rows with buses that exceeded 50 km/h.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :return: dataframe containing rows with data for buses that exceeded 50 km/h.
    """
    result = pd.DataFrame({"Lines": [], "Lon": [], "VehicleNumber": [], "Time": [], "Lat": [], "Brigade": []})
    for i in range(1, len(dataset)):
        df = exceed_50(dataset, i-1, i)
        result = pd.concat([result, df])
    return result


def how_many_exceeded_50(dataset):
    """
    Counts unique buses that exceeded 50 km/h for the given dataset.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :return: number of unique buses that exceeded 50 km/h.
    """
    df = all_exceeding_50(dataset)
    return df["VehicleNumber"].nunique()


def near(place1_lat, place1_lon, place2_lat, place2_lon, radius_in_km):
    """
    Checks if two places are near each other. By 'near' we understand that the distance between them is less than the given radius.
    :param place1_lat: latitude of the first place (numeric).
    :param place1_lon: longitude of the first place (numeric).
    :param place2_lat: latitude of the second place (numeric).
    :param place2_lon: longitude of the second place (numeric).
    :param radius_in_km: the maximal distance between two places such that we can call them 'near each other'.
    :return: True or False.
    """
    return geopy.distance.geodesic((place1_lat, place1_lon), (place2_lat, place2_lon)).km < radius_in_km


def all_vehicles_near(dataset, place_lat, place_lon, radius):
    """
    For the given dataset returns dataframe containing rows with vehicles that were near some place. By 'near' we understand in a circle with its center in this location and with given radius.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param place_lat: latitude of the place of interest (numeric).
    :param place_lon: longitude of the place of interest (numeric).
    :param radius: radius of circle around the place.
    :return: dataframe containing data for vehicles that were near given place
    """
    result = pd.DataFrame({"Lines": [], "Lon": [], "VehicleNumber": [], "Time": [], "Lat": [], "Brigade": []})
    for i in range(1, len(dataset)):
        df = pd.merge(dataset[i-1], inst_velocity(dataset, i-1, i), on=["VehicleNumber"], how="inner")
        df = df[list(map(functools.partial(near, place2_lat=place_lat, place2_lon=place_lon, radius_in_km=radius), df["Lat"], df["Lon"]))]
        result = pd.concat([result, df])
    return result


def percentage_exceeding_50(dataset, place_lat, place_lon, radius):
    """
    Returns percentage of buses exceeding 50 km/h near some place for the given dataset. By 'near' we understand in a circle with its center in the given location and with given radius.
    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param place_lat: latitude of the place of interest (numeric).
    :param place_lon: longitude of the place of interest (numeric).
    :param radius: radius of circle around the place (numeric).
    :return: percentage of buses exceeding 50 km/h.
    """
    df_near = all_vehicles_near(dataset, place_lat, place_lon, radius)
    how_many_near = df_near["VehicleNumber"].nunique()
    df_exceeding_50 = df_near[df_near["Velocity"] > 50]
    how_many_exceeding = df_exceeding_50["VehicleNumber"].nunique()
    try:
        return how_many_exceeding/how_many_near
    except ZeroDivisionError:
        print("No busus in this region for given dataset")


def plot_on_map(dataframe, title, path_to_map):
    """
    For a given dataframe with locations of buses plots these locations on the map of Warsaw.
    :param dataframe: A dataframe containing columns "Lon" and "Lat".
    :param title: Title for the plot.
    :param path_to_map: here the best idea is to use the map provided with the package, i.e. set this parameter to os.path.dirname(buses_warsaw.__file__)+'/map.png'
    :return: None.
    """
    df = dataframe[["Lon", "Lat"]]
    Box = ((20.8000, 21.3000, 52.1000, 52.3500))
    ruh_m = plt.imread(path_to_map)
    fig, ax = plt.subplots()
    ax.scatter(df["Lon"], df["Lat"], zorder=1, alpha=1, c='b', s=10)
    ax.set_title(title)
    ax.set_xlim(Box[0], Box[1])
    ax.set_ylim(Box[2], Box[3])
    ax.imshow(ruh_m, zorder=0, extent = Box, aspect='equal')
    plt.show()


def load_bus_stops(api_key):
    """
    Downloads data with locations of bus stops from https://api.um.warszawa.pl/. One must provide their personal api key to get the data.
    :param api_key: personal api key.
    :return: pandas.DataFrame with downloaded data.
    """
    df = pd.DataFrame({"zespol": [], "slupek": [], "nazwa_zespolu": [], "id_ulicy": [], "szer_geo": [], "dlug_geo": [], "kierunek": []})
    url = 'https://api.um.warszawa.pl/api/action/dbstore_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey={}&type=1'.format(str(api_key))
    with urllib.request.urlopen(url) as url2:
        s = str(url2.read())
    s = s.split(']}')
    s = s[0:len(s)-2]
    for i in range(len(s)):
        if not s[i].startswith(',{'):
            s[i] = s[i][s[i].find('"value"')-1:]
        spl = s[i].split('"')
        spl = list(spl[i] for i in [5, 13, 21, 29, 37, 45, 53])
        spl = pd.DataFrame([spl], columns=["zespol", "slupek", "nazwa_zespolu", "id_ulicy", "szer_geo", "dlug_geo", "kierunek"])
        df = pd.concat([df, spl])
    if df.empty:
        print("Api key is not correct!")
    return df


def is_not_float(value):
    """
    Checks if a value can be converted to float.
    :param value: string to be converted.
    :return: True or False.
    """
    try:
        float(value)
        return False
    except ValueError:
        return True


def load_bus_stops_from_file(directory, name_of_file):
    """
    Loads locations of bus stops from file.
    :param directory: Directory with file.
    :param name_of_file: name of file. File must be tab-separated and contain columns: "zespol", "slupek", "nazwa_zespolu", "id_ulicy", "szer_geo", "dlug_geo", "kierunek"; first row will be skipped.
    :return: pandas.Dataframe with data loaded from file.
    """
    with open(directory+"/"+name_of_file, "r") as f:
        df = pd.read_csv(f, delimiter="\t", names=["zespol", "slupek", "nazwa_zespolu", "id_ulicy", "szer_geo", "dlug_geo", "kierunek"], skiprows=1, dtype={'zespol': object, 'slupek': object})
    try:
        df["dlug_geo"] = pd.to_numeric(df["dlug_geo"])
    except ValueError:
        df.loc[list(map(is_not_float, df["dlug_geo"])), "dlug_geo"] = np.NaN
    try:
        df["szer_geo"] = pd.to_numeric(df["szer_geo"])
    except ValueError:
        df.loc[list(map(is_not_float, df["szer_geo"])), "szer_geo"] = np.NaN
    return df


def load_schedule(bus_stop_id, bus_stop_number, line, api_key):
    """
    Downloads schedule from https://api.um.warszawa.pl/ for the given bus stop and line. One must provide their personal api key to get the data.
    :param bus_stop_id: Bus stop id (numeric).
    :param bus_stop_number: Bus stop number (string).
    :param line: Line number (numeric).
    :param api_key: personal api key.
    :return: pandas.DataFrame with downloaded data.
    """
    df = pd.DataFrame({"symbol_2": [], "symbol_1": [], "brygada": [], "kierunek": [], "trasa": [], "czas": []})
    url = 'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId={}&busstopNr={}&line={}&apikey={}&type=1'.format(str(bus_stop_id), str(bus_stop_number), str(line), str(api_key))
    with urllib.request.urlopen(url) as url2:
        s = str(url2.read())
    s = s.split(']}')
    s = s[1:len(s)-2]
    for i in range(len(s)):
        if not s[i].startswith(',{'):
            s[i] = s[i][s[i].find('"value"')-1:]
        spl = s[i].split('"')
        spl = list(spl[i] for i in [5, 13, 21, 29, 37, 45])
        spl = pd.DataFrame([spl], columns=["symbol_2", "symbol_1", "brygada", "kierunek", "trasa", "czas"])
        df = pd.concat([df, spl])
    return df


def is_not_datetime(value):
    """
    Checks if a value can be converted to datetime.
    :param value: string to convert.
    :return True or False.
    """
    try:
        datetime.strptime(value, "%H:%M:%S").date()
        return False
    except ValueError:
        return True


def load_schedule_from_file(directory, name_of_file):
    """

    :param directory: Directory with file.
    :param name_of_file: Name of file with data. It must be tab-separated and contain columns : "symbol-2", "symbol-1", "brygada", "kierunek", "trasa", "czas" and no headers.
    :return: pandas.DataFrame with data from input file.
    """
    with open(directory+"/"+name_of_file, "r") as f:
        df = pd.read_csv(f, delimiter="\t", names=["symbol_2", "symbol_1", "brygada", "kierunek", "trasa", "czas"], encoding='utf8')
    try:
        df["czas"] = pd.to_datetime(df["czas"], format="%H:%M:%S")
    except ValueError:
        df.loc[list(map(is_not_datetime, df["czas"])), "czas"] = np.NaN
    return df


def is_on_time(dataset, locations_dataset, bus_stop_name, bus_stop_number, line, api_key, verbose=True):
    """

    :param dataset: List of pandas.DataFrames, each corresponding to one moment of time. Each of these dataframes should have columns: "Lines", "Lon", "VehicleNumber", "Time", "Lat", "Brigade".
    :param locations_dataset: pandas.DataFrame containing locations of bus stops. Columns: "zespol", "slupek", "nazwa_zespolu", "id_ulicy", "szer_geo", "dlug_geo", "kierunek".
    :param bus_stop_name: Name of the bus stop given, for example: "Marszałkowska".
    :param bus_stop_number: Number of the bus stop given as string, for example "01".
    :param line: Number of line, for example 520.
    :param api_key: personal api key.
    :param verbose: If True, additional information about number of all buses and number of punctual buses will be printed. Default is True.
    :return: Fraction of buses that were on time for the given dataset, line and bus stop.
    """
    bs = locations_dataset[(locations_dataset["nazwa_zespolu"] == bus_stop_name.encode("unicode-escape").decode("utf-8").replace('\\', '\\\\')) & (locations_dataset["slupek"] == bus_stop_number)]
    try:
        expected_lon = bs["dlug_geo"].iloc[0]
        expected_lat = bs["szer_geo"].iloc[0]
        bus_stop_id = bs["zespol"].iloc[0]
        schedule = load_schedule(bus_stop_id=str(bus_stop_id), bus_stop_number=str(bus_stop_number), line=str(line), api_key=api_key)
        our_line = pd.DataFrame({"Lines": [], "Lon": [], "VehicleNumber": [], "Time": [], "Lat": [], "Brigade": []})
        for i in range(len(dataset)):
            our_line = pd.concat([our_line, dataset[i][dataset[i]["Lines"] == str(line)]])
        earliest = min(our_line["Time"]).strftime('%H:%M:%S')
        latest = max(our_line["Time"]).strftime('%H:%M:%S')
        expected_time = schedule[(schedule["czas"] > earliest) & (schedule["czas"] < latest)]
        on_time = list()
        for i in range(expected_time.shape[0]):
            tm = expected_time["czas"].iloc[i]
            tm = datetime.strptime(tm, "%H:%M:%S")
            near_tm = pd.DataFrame({"Lines": [], "Lon": [], "VehicleNumber": [], "Time": [], "Lat": [], "Brigade": []})
            for j in range(our_line.shape[0]):
                tm = tm.replace(year=our_line["Time"].iloc[j].year, month=our_line["Time"].iloc[j].month, day=our_line["Time"].iloc[j].day)
                if ((our_line["Time"].iloc[j] - tm) < timedelta(minutes=1)) & ((our_line["Time"].iloc[j] - tm) >= timedelta(seconds=0)):
                    near_tm = pd.concat([near_tm, our_line.iloc[[j]]])
            near_stop = near_tm[list(map(functools.partial(near, place2_lat=expected_lat, place2_lon=expected_lon, radius_in_km=0.05), near_tm["Lat"], near_tm["Lon"]))]
            on_time.append(near_stop.empty)
        if verbose:
            print('There should be {} such bus(es) according to schedule in the analysed time period. {} of them was/were on time.'.format(str(len(on_time)), str(sum(on_time))))
            print('Fraction of punctual buses for the given bus stop and line: ')
        return sum(on_time)/len(on_time)
    except TypeError:
        print("The input data is not correct! This line does not run in this region. /Your api key is not correct.")
    except IndexError:
        print("The input data is not correct! No such bus stop.")
