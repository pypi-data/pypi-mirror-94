from parchments.core.validation import is_valid_list_choice, is_valid_date_or_datetime
from parchments.core.block import Block
from parchments.core.choices import VALUE_TYPE_CHOICES


class Row:
    block_order_list = list()
    period_iteration = None
    over_period_iteration = None

    def __init__(self, name, value_type, value_decimals, period_iteration, over_period_iteration):
        if is_valid_list_choice(value_type, VALUE_TYPE_CHOICES):
            self.value_type = value_type
        self.value_decimals = value_decimals
        self.name = name
        self.period_iteration = period_iteration
        self.over_period_iteration = over_period_iteration
        self.block_dict = dict()

    def create_block(self, period_key, value):
        self.block_dict[period_key] = Block(period_key, value, self.value_type, self.value_decimals)
        if period_key not in self.block_order_list:
            self.block_order_list.append(period_key)
        self.block_order_list.sort()

    def update_row(self):
        for loop_index, block_order in enumerate(self.block_order_list):
            if loop_index + 1 < len(self.block_order_list):
                self.block_dict[block_order].compare_projected(self.block_dict[self.block_order_list[loop_index + 1]])
            else:
                self.block_dict[block_order].compare_projected(self.block_dict[block_order])
            if self.over_period_iteration == 'year':
                if str(int(block_order) + 10000) in self.block_order_list:
                    self.block_dict[block_order].compare_over_projected(
                        self.block_dict[str(int(block_order) + 10000)])
                else:
                    self.block_dict[block_order].compare_over_projected(self.block_dict[block_order])

    def as_dict(self):
        row_list = list()
        for block_order in self.block_order_list:
            row_list.append(self.block_dict[block_order].as_dict())
        return row_list
