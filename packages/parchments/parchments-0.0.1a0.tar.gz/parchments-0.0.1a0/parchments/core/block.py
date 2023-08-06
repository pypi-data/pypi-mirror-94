from parchments.core.choices import VALUE_TYPE_CHOICES


class Block:

    def __init__(self, period_key, value, value_type: str, decimal_places=0, actual_number=True):
        self.period_key = period_key
        self.value = value
        self.value_type = value_type
        self.decimal_places = decimal_places
        self.actual_number = actual_number
        self.growth_amount = 0.00

    def to_dict(self):
        block_dict = {
            'value': self.value,
            'verbose': self.verbose(),
            'growth_amount': self.growth_amount,
        }
        return block_dict

    def verbose(self):
        if self.value_type == 'dollar':
            return '${:,.2f}'.format(self.value)
        elif self.value_type == 'percentage':
            return '{:,.4f}%'.format((self.value * 100))
        elif self.value_type == 'int':
            return '{:,.0f}'.format(self.value)
        else:
            return self.value

    def compare_historical(self, historical_block):
        self.growth_amount = self.value - historical_block.value

    def compare_projected(self, projected_block):
        projected_block.compare_historical(self)

    def compare_historical_over(self, historical_over_block):
        pass

    def compare_projected_over(self, projected_block):
        pass