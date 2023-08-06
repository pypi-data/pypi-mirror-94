from parchments.core.row import Row
from parchments.core.core import period_key
from parchments.core.validation import is_valid_date_or_datetime
from parchments.core.choices import PERIOD_ITERATION_CHOICES, OVER_PERIOD_ITERATION_CHOICES


class Grid:

    def __init__(self, row_index, period_iteration='month', over_period_iteration='year'):
        if period_iteration in PERIOD_ITERATION_CHOICES:
            self.period_iteration = period_iteration
        else:
            raise SyntaxError('Invalid period iteration choices %s' % PERIOD_ITERATION_CHOICES)

        if over_period_iteration in OVER_PERIOD_ITERATION_CHOICES:
            self.over_period_iteration = over_period_iteration
        else:
            raise SyntaxError('Invalid layer iteration choices %s' % OVER_PERIOD_ITERATION_CHOICES)

        self.row_index = row_index

        self.row_dict = dict()
        for row in self.row_index:
            self.row_dict[row[0]] = Row(row[0], row[1], row[2], self.period_iteration, self.over_period_iteration)

    def add_period(self, period, value_list):
        if is_valid_date_or_datetime(period):
            if type(value_list) is list:
                for loop_index, row in enumerate(self.row_index):
                    self.row_dict[row[0]].create_block(period_key(period, self.period_iteration), value_list[loop_index])
                    self.row_dict[row[0]].update_row()

    def to_dict(self):
        grid_dict = dict()
        grid_dict['row_data'] = dict()
        for row in self.row_index:
            # Todo: This is a bit lazy for assignment of block order list
            grid_dict['row_data'][row[0]] = self.row_dict[row[0]].as_dict()
            grid_dict['column_index'] = self.row_dict[row[0]].block_order_list
        return grid_dict

