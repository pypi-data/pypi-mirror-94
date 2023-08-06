from decimal import Decimal

class Value:

    def __init__(self, value, value_type, decimals=2):
        self.data = {
            'raw': value,
            'clean': value,
            'verbose': self.verbose(value, value_type),
            'type': value_type,
            'decimals': decimals,
        }

    def verbose(self, value, value_type):
        if value == 0 or value == 0.0 or value == Decimal(0.0):
            return '-'
        elif value_type == 'dollar':
            return '${:,.2f}'.format(value)
        elif value_type == 'percentage':
            return '{:,.4f}%'.format((value * 100))
        elif value_type == 'int':
            return '{:,.0f}'.format(value)
        else:
            return value

    def as_dict(self):
        return self.data