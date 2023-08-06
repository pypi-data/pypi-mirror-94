from datetime import datetime


def period_key(period: datetime, iteration: str):
    if iteration == 'year':
        return '%s' % period.year
    if iteration == 'month':
        return '%s-%s' % (period.year, period.month)
    if iteration == 'day':
        return '%s-%s-%s' % (period.year, period.month, period.day)

