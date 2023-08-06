import unittest
from buses_warsaw import buses
import pandas as pd
import os
import os.path


class TestBuses(unittest.TestCase):

    def test_load(self):
        result = buses.load('b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIsNone(buses.load('a'))

    def test_collect_data(self):
        result = buses.collect_data(2, 60, 'b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], pd.DataFrame)
        result2 = buses.collect_data(2, 60, 'a')
        self.assertIsNone(result2[0])

    def test_load_from_files(self):
        result = buses.load_from_files(os.path.dirname(os.getcwd())+'/buses_warsaw/data', 'data')
        self.assertIsNot(result[0], [])
        self.assertEqual(result[0]["Lines"].dtypes, 'object')
        self.assertEqual(result[0]["Lon"].dtypes, 'float64')
        self.assertEqual(result[0]["VehicleNumber"].dtypes, 'int64')
        self.assertEqual(result[0]["Time"].dtypes, '<M8[ns]')
        self.assertEqual(result[0]["Lat"].dtypes, 'float64')
        self.assertEqual(result[0]["Brigade"].dtypes, 'object')
        self.assertRaises(ValueError, buses.load_from_files, os.path.dirname(os.getcwd())+'/buses_warsaw/data', 'bus_stops')

    def test_distance(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd())+'/buses_warsaw/data', 'data')
        dist = buses.distance(dataset, 0, len(dataset)-1)
        self.assertTrue(dist["Distance"].ge(0).all())
        self.assertTrue(dist["Distance"].le(70).all())

    def test_time_difference(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', 'data')
        t = buses.time_difference(dataset, 0, len(dataset)-1)
        self.assertTrue(t["Time_difference"].ge(0).all())

    def test_inst_velocity(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd())+'/buses_warsaw/data', 'data')
        v = buses.inst_velocity(dataset, 0, len(dataset)-1)
        self.assertTrue(v["Velocity"][v["Velocity"].notna()].ge(0).all())
        self.assertTrue(v["Velocity"][v["Velocity"].notna()].le(200).all())

    def test_exceed_50(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd())+'/buses_warsaw/data', 'data')
        result = buses.exceed_50(dataset, 0, len(dataset)-1)
        self.assertTrue(result["Velocity"].ge(50).all())

    def test_all_exceeding_50(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', 'data')
        result = buses.all_exceeding_50(dataset)
        self.assertTrue(result["Velocity"].ge(50).all())

    def test_how_many_exceeded_50(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', 'data')
        result = buses.how_many_exceeded_50(dataset)
        self.assertTrue(result > 0)

    def test_near(self):
        result = buses.near(52, 21, 52, 21, 1)
        self.assertTrue(result)
        result = buses.near(52, 21, 60, 21, 1)
        self.assertFalse(result)

    def test_percentage_exceeding_50(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', 'data')
        result = buses.percentage_exceeding_50(dataset, 52, 21, 100)
        self.assertTrue(result >= 0 and result <= 1)

    def test_load_bus_stops(self):
        result = buses.load_bus_stops('b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(buses.load_bus_stops('a').empty)

    def test_load_bus_stops_from_file(self):
        result = buses.load_bus_stops_from_file(os.path.dirname(os.getcwd())+'/buses_warsaw/data', 'bus_stops_0.txt')
        self.assertIsNotNone(result)
        self.assertEqual(result["zespol"].dtypes, 'object')
        self.assertEqual(result["slupek"].dtypes, 'object')
        self.assertEqual(result["nazwa_zespolu"].dtypes, 'object')
        self.assertEqual(result["id_ulicy"].dtypes, 'object')
        self.assertEqual(result["szer_geo"].dtypes, 'object')
        self.assertEqual(result["dlug_geo"].dtypes, 'object')
        self.assertEqual(result["kierunek"].dtypes, 'object')

    def test_load_schedule(self):
        result = buses.load_schedule(7009, '01', 523, 'b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(buses.load_schedule(7009, '01', 523, 'a').empty)
        self.assertTrue(buses.load_schedule(7009, '99', 523, 'a').empty)

    def test_load_schedule_from_file(self):
        result = buses.load_schedule_from_file(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', 'schedule_7009_01_523_0.txt')
        self.assertIsNotNone(result)
        self.assertEqual(result["symbol_2"].dtypes, 'float64')
        self.assertEqual(result["symbol_1"].dtypes, 'float64')
        self.assertEqual(result["brygada"].dtypes, 'int64')
        self.assertEqual(result["kierunek"].dtypes, 'object')
        self.assertEqual(result["trasa"].dtypes, 'object')
        self.assertEqual(result["czas"].dtypes, 'datetime64[ns]')

    def test_is_on_time(self):
        dataset = buses.load_from_files(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', 'data')
        locations_dataset = buses.load_bus_stops_from_file(os.path.dirname(os.getcwd()) + '/buses_warsaw/data', "bus_stops_0.txt")
        result = buses.is_on_time(dataset, locations_dataset, "Marszałkowska", "01", 520, api_key='b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertTrue(result <= 1)
        result = buses.is_on_time(dataset, locations_dataset, "Marszałkowska", "01", 521, api_key='b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertIsNone(result)
        result = buses.is_on_time(dataset, locations_dataset, "Marszałkowska", "99", 520, api_key='b2b6deb9-bb03-4279-b25d-55fa1bb97690')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
