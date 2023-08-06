from parchments.core.value import Value


class Block:

    def __init__(self, period, value, value_type: str, decimal_places=0, actual_number=True):
        self.period = period
        self.value = value
        self.value_type = value_type
        self.decimal_places = decimal_places
        self.actual_number = actual_number
        self.data_dict = {
            'actual_number': self.actual_number,
            'period_key': self.period.key,
            'value_amount': Value(value, value_type),
        }

    def as_dict(self):
        block_dict = dict()
        for key, val in self.data_dict.items():
            if type(val) is Value:
                block_dict[key] = val.as_dict()
            else:
                block_dict[key] = val
        return block_dict

    def as_list(self):
        block_list = list()
        for key, val in self.data_dict.items():
            if type(val) is Value:
                block_list.append(val.as_list())
            else:
                block_list.append(val)
        return block_list

    def compare_historical(self, historical_block):
        if self.value_type != 'string':
            self.data_dict['growth_amount'] = Value(self.value - historical_block.value, self.value_type, 2)
            try:
                self.data_dict['growth_percentage'] = Value(self.data_dict['growth_amount'].data_dict['raw'] / historical_block.value, 'percentage', 4)
            except ZeroDivisionError:
                self.data_dict['growth_percentage'] = 0

    def compare_projected(self, projected_block):
        projected_block.compare_historical(self)

    def compare_over_historical(self, over_historical_block):
        if self.value_type != 'string':
            self.data_dict['over_growth_amount'] = Value(self.value - over_historical_block.value, self.value_type, 2)
            try:
                self.data_dict['over_growth_percentage'] = Value(self.data_dict['over_growth_amount'].data_dict['raw'] / over_historical_block.value, 'percentage', 4)
            except ZeroDivisionError:
                self.data_dict['growth_percentage'] = 0

    def compare_over_projected(self, over_projected_block):
        over_projected_block.compare_over_historical(self)

    def calculate_growth(self, value1, value2):
        pass