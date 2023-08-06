import unittest
import parchments
import datetime
import decimal

test_index = (
    ('goats', 'int', 0),
    ('price', 'dollar', 2),
    ('value', 'percentage', 4),
    ('names', 'string', 0),
)

test_grid = parchments.Grid(test_index)


class TestGrid(unittest.TestCase):

    def test_grid_add_period(self, period=datetime.datetime.now(), index=[1, 22.2, 0.70, 'bob']):
        try:
            test_grid.add_period(datetime.datetime.now(), [1, 22.2, 0.70, 'bob'])
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_add_period_with_datetime_input(self):
        self.test_grid_add_period(period=datetime.datetime.now())

    def test_add_period_with_date_input(self):
        self.test_grid_add_period(period=datetime.date.today())

    def test_add_period_with_decimal_input(self):
        self.test_grid_add_period(index=[1, decimal.Decimal(22.2), 0.70, 'bob'])

    def test_add_period_with_float_input(self):
        self.test_grid_add_period(index=[1, float(22.2), 0.70, 'bob'])

    def test_add_period_with_zero_division_input(self):
        self.test_grid_add_period(index=[1, 22.0, 0.70, 'bob'])
        self.test_grid_add_period(index=[1, 0.0, 0.70, 'bob'])
