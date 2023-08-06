from datetime import datetime


def period_key(period: datetime, iteration: str):
    if iteration == 'year':
        return '%s0101' % period.strftime('%Y')
    if iteration == 'month':
        return '%s01' % period.strftime('%Y%m')
    if iteration == 'day':
        return '%s' % period.strftime('%Y%m%d')

