from parchments.core.value import Value


class Block:

    def __init__(self, period, value, value_type: str, decimal_places=0, actual_number=True):
        self.period = period
        self.value = value
        self.value_type = value_type
        self.decimal_places = decimal_places
        self.actual_number = actual_number
        self.data = {
            'actual_number': self.actual_number,
            'period_key': self.period.key,
            'value_amount': Value(value, value_type).as_dict(),
        }

    def as_dict(self):
        return self.data

    def compare_historical(self, historical_block):
        if self.value_type != 'string':
            self.data['growth_amount'] = Value(self.value - historical_block.value, self.value_type, 2).as_dict()
            self.data['growth_percentage'] = Value(self.data['growth_amount']['raw'] / historical_block.value, 'percentage', 4).as_dict()

    def compare_projected(self, projected_block):
        projected_block.compare_historical(self)

    def compare_over_historical(self, over_historical_block):
        if self.value_type != 'string':
            self.data['over_growth_amount'] = Value(self.value - over_historical_block.value, self.value_type, 2).as_dict()
            self.data['over_growth_percentage'] = Value(self.data['over_growth_amount']['raw'] / over_historical_block.value, 'percentage', 4).as_dict()

    def compare_over_projected(self, over_projected_block):
        over_projected_block.compare_over_historical(self)

    def calculate_growth(self, value1, value2):
        pass