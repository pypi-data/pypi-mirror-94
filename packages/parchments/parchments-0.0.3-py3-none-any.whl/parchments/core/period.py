from datetime import date, datetime


class Period:

    def __init__(self, date_or_datetime, iteration):
        if type(date_or_datetime) is date:
            self.datetime = datetime.combine(date_or_datetime, datetime.min.time())
        elif type(date_or_datetime is datetime):
            self.datetime = date_or_datetime
        else:
            raise ValueError('Invalid period. Must be a datetime.date or datetime.datetime')

        self.iteration = iteration

        if self.iteration == 'year':
            self.key = '%s0101' % self.datetime.strftime('%Y')
        if self.iteration == 'month':
            self.key = '%s01' % self.datetime.strftime('%Y%m')
        if self.iteration == 'day':
            self.key = '%s' % self.datetime.strftime('%Y%m%d')
