import unittest
import pytplot
import numpy as np
import datetime


class TestDocstingExamples(unittest.TestCase):
    """
    Automated tests of docstring examples
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        # Delete all tplot variables
        pytplot.del_data('*')

    def test_pytplot_options_execution(self):
        """
        Test to ensure the pytplot.options related code executes without errors.
        """
        try:
            # Setup for the first part of the test
            x_data = [1, 2, 3, 4, 5]
            y_data = [1, 2, 3, 4, 5]
            pytplot.store_data("Variable1", data={'x': x_data, 'y': y_data})
            pytplot.options('Variable1', 'yrange', [2, 4])
            pytplot.options('Variable1', 'ylog', 1)

            # Setup for the second part of the test involving multi-dimensional data
            y_data = np.random.rand(5, 4, 3)
            v1_data = [0, 1, 3, 4]
            v2_data = [1, 2, 3]
            pytplot.store_data("Variable2", data={'x': x_data, 'y': y_data, 'v1': v1_data, 'v2': v2_data})
            pytplot.options('Variable2', 'spec', 1)
            pytplot.options("Variable2", "spec_dim_to_plot", 'v2')
            pytplot.options("Variable2", "spec_slices_to_use", {'v1': 0})

            # If we reach this point, it means no exceptions were raised
            no_errors = True
        except Exception as e:
            no_errors = False

        self.assertTrue(no_errors, "Execution of pytplot.options related code resulted in errors.")

    def test_pytplot_get_ylimits(self):
        """
        Test to ensure the pytplot.get_ylimits code executes without errors, and returns correct type and values.
        """
        x_data = [1, 2, 3, 4, 5]
        y_data = [1, 2, 3, 4, 5]
        pytplot.store_data("Variable1", data={'x': x_data, 'y': y_data})
        y1, y2 = pytplot.get_ylimits("Variable1")

        self.assertIsInstance(y1, int)
        self.assertIsInstance(y2, int)
        self.assertEqual(y1, 1)
        self.assertEqual(y2, 5)

    def test_pytplot_time_float_one(self):
        """
        Test to ensure the pytplot.time_double.time_float_one code executes without errors, and returns and values.
        Test for one or no parameters
        """
        time_now = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds();
        self.assertAlmostEqual(pytplot.time_float_one(), time_now, delta=1)
        self.assertEqual(pytplot.time_float_one('2023-03-25 12:00:00'), 1679745600.0)

    def test_pytplot_time_float(self):
        """
        Test to ensure the pytplot.time_double.time_float code executes without errors, and returns and values.
        Test for one, list or no parameters
        """
        time_now = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
        self.assertAlmostEqual(pytplot.time_float(), time_now, delta=1)
        self.assertEqual(pytplot.time_float('2023-03-25 12:00:00'), 1679745600.0)
        self.assertEqual(pytplot.time_float(['2023-03-25 12:00:00', '2023-03-26 12:00:00']),
                         [1679745600.0, 1679832000.0])

    def test_pytplot_time_double(self):
        """
        Test to ensure the pytplot.time_double code executes without errors, and returns and values.
        Test for one, list or no parameters
        """
        time_now = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds();
        self.assertAlmostEqual(pytplot.time_double(), time_now, delta=1)
        self.assertEqual(pytplot.time_double('2023-03-25 12:00:00'), 1679745600.0)
        self.assertEqual(pytplot.time_double(['2023-03-25 12:00:00', '2023-03-26 12:00:00']),
                         [1679745600.0, 1679832000.0])

    def test_pytplot_time_string_one(self):
        """
        Test to ensure the pytplot.time_string.time_string_one code executes without errors, and returns and values.
        Test for no parameters, one parameter, and one parameters with a format
        """

        # This must be executed fast enough for comparison
        now_str = pytplot.time_string_one()
        now_str_no_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(now_str[:-7], now_str_no_ms)
        self.assertEqual(pytplot.time_string_one(1679745600.0), '2023-03-25 12:00:00.000000')
        self.assertEqual(pytplot.time_string_one(1679745600.0, fmt="%Y-%m-%d"), '2023-03-25')

    def test_pytplot_time_string(self):
        """
        Test to ensure the pytplot.time_string.time_string code executes without errors, and returns and values.
        Test for no parameters, one parameter, and one parameters with a format
        """

        # This must be executed fast enough for comparison
        now_str = pytplot.time_string()
        now_str_no_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(now_str[:-7], now_str_no_ms)
        self.assertEqual(pytplot.time_string(1679745600.0), '2023-03-25 12:00:00.000000')
        self.assertEqual(pytplot.time_string(1679745600.0, fmt="%Y-%m-%d"), '2023-03-25')
        self.assertEqual(pytplot.time_string([1679745600.0, 1679832000.0], fmt="%Y-%m-%d %H:%M:%S"),
                         ['2023-03-25 12:00:00', '2023-03-26 12:00:00'])

    def test_pytplot_time_datetime(self):
        """
        Test to ensure the pytplot.time_datetime code executes without errors, and returns and values.
        Test for one, list or no parameters
        """
        test_datetime = datetime.datetime(2023, 3, 25, 12, 0, tzinfo=datetime.timezone.utc)
        test_datetime_list = [datetime.datetime(2023, 3, 25, 12, 0, tzinfo=datetime.timezone.utc),
                              datetime.datetime(2023, 3, 26, 12, 0, tzinfo=datetime.timezone.utc)]
        test_datetime_offset = datetime.datetime(2023, 3, 25, 6, 0,
                                                 tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=64800)))

        self.assertEqual(pytplot.time_datetime(1679745600.0), test_datetime)
        self.assertEqual(pytplot.time_datetime('2023-03-25 12:00:00'), test_datetime)

        self.assertEqual(pytplot.time_datetime([1679745600.0, 1679832000.0]), test_datetime_list)
        self.assertEqual(pytplot.time_datetime(['2023-03-25 12:00:00', '2023-03-26 12:00:00']), test_datetime_list)

        self.assertEqual(pytplot.time_datetime(1679745600.0, tz=datetime.timezone(datetime.timedelta(hours=-6))),
                         test_datetime_offset)

        self.assertLessEqual(abs(pytplot.time_datetime() - datetime.datetime.now()), datetime.timedelta(seconds=1))


if __name__ == '__main__':
    unittest.main()
