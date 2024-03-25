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
        time_now = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds();
        self.assertAlmostEqual(pytplot.time_float_one(), time_now, delta=1)
        self.assertEqual(pytplot.time_float_one('2023-03-25 12:00:00'), 1679745600.0)

    def test_pytplot_time_float(self):
        """
        Test to ensure the pytplot.time_double.time_float code executes without errors, and returns and values.
        Test for one, list or no parameters
        """
        time_now = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds();
        self.assertAlmostEqual(pytplot.time_float(), time_now, delta=1)
        self.assertEqual(pytplot.time_float('2023-03-25 12:00:00'), 1679745600.0)
        self.assertEqual(pytplot.time_float(['2023-03-25 12:00:00', '2023-03-26 12:00:00']),  [1679745600.0, 1679832000.0])


    def test_pytplot_time_double(self):
        """
        Test to ensure the pytplot.time_double code executes without errors, and returns and values.
        Test for one, list or no parameters
        """
        time_now = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds();
        self.assertAlmostEqual(pytplot.time_double(), time_now, delta=1)
        self.assertEqual(pytplot.time_double('2023-03-25 12:00:00'), 1679745600.0)
        self.assertEqual(pytplot.time_double(['2023-03-25 12:00:00', '2023-03-26 12:00:00']), [1679745600.0, 1679832000.0])


if __name__ == '__main__':
    unittest.main()
