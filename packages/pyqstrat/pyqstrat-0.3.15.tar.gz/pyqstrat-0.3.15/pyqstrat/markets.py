import re
import datetime
from dateutil._common import weekday
import dateutil.relativedelta as rd
import numpy as np
from pyqstrat.holiday_calendars import Calendar, get_date_from_weekday
from typing import Tuple, Mapping

FUTURE_CODES_INT = {'F': 1, 'G': 2, 'H': 3, 'J': 4, 'K': 5, 'M': 6, 'N': 7, 'Q': 8, 'U': 9, 'V': 10, 'X': 11, 'Z': 12}
FUTURES_CODES_INVERTED: Mapping[int, str] = {v: k for k, v in FUTURE_CODES_INT.items()}

FUTURE_CODES_STR = {'F': 'jan', 'G': 'feb', 'H': 'mar', 'J': 'apr', 'K': 'may', 'M': 'jun', 
                    'N': 'jul', 'Q': 'aug', 'U': 'sep', 'V': 'oct', 'X': 'nov', 'Z': 'dec'}


def future_code_to_month(future_code: str) -> str:
    '''
    Given a future code such as "X", return the month abbreviation, such as "nov"
    
    Args:
        future_code (str): the one letter future code
        
    >>> future_code_to_month('X')
    'nov'
    '''
    assert len(future_code) == 1, f'Future code must be a single character: {future_code}'
    if future_code not in FUTURE_CODES_STR: raise Exception(f'unknown future code: {future_code}')
    return FUTURE_CODES_STR[future_code]
    
    if future_code not in FUTURE_CODES_INT: raise Exception(f'unknown future code: {future_code}')
    return FUTURE_CODES_INT[future_code]


def future_code_to_month_number(future_code: str) -> int:
    '''
    Given a future code such as "X", return the month number (from 1 - 12)
    
    Args:
        future_code (str): the one letter future code
        
    >>> future_code_to_month_number('X')
    11
    '''
    assert len(future_code) == 1, f'Future code must be a single character: {future_code}'
    if future_code not in FUTURE_CODES_INT: raise Exception(f'unknown future code: {future_code}')
    return FUTURE_CODES_INT[future_code]


def get_future_code(month: int) -> str:
    '''
    Given a month number such as 3 for March, return the future code for it, e.g. H
    >>> get_future_code(3)
    'H'
    '''
    return FUTURES_CODES_INVERTED[month]


class EminiFuture:
    
    calendar = Calendar.get_calendar(Calendar.NYSE)

    @staticmethod
    def get_current_symbol(curr_date: datetime.date) -> str:
        '''
        >>> assert(EminiFuture.get_current_symbol(datetime.date(2019, 3, 14)) == 'ESH9')
        >>> assert(EminiFuture.get_current_symbol(datetime.date(2019, 3, 15)) == 'ESM9')
        >>> assert(EminiFuture.get_current_symbol(datetime.date(2020, 3, 14)) == 'ESH0')
        '''
        year = curr_date.year
        month = curr_date.month
        day = curr_date.day
        third_friday_ = EminiFuture.calendar.third_friday_of_month(month, year)
        third_friday: datetime.date = third_friday_.astype(datetime.date)  # type: ignore
        if month < 3 or (month == 3 and day < third_friday.day): month_str = 'H'
        elif month < 6 or (month == 6 and day < third_friday.day): month_str = 'M'
        elif month < 9 or (month == 9 and day < third_friday.day): month_str = 'U'
        elif month < 12 or (month == 12 and day < third_friday.day): month_str = 'Z'
        else:
            month_str = 'H'
            year += 1
        base = 2010 if year < 2020 else 2020
        fut_symbol = 'ES' + month_str + str(year - base)
        return fut_symbol

    @staticmethod
    def get_previous_symbol(curr_future_symbol: str) -> str:
        '''
        >>> assert(EminiFuture.get_previous_symbol('ESH9') == 'ESZ8')
        '''
        month = curr_future_symbol[2]
        year = int(curr_future_symbol[3])
        prev_month = {'H': 'Z', 'M': 'H', 'U': 'M', 'Z': 'U'}[month]
        prev_year = year if prev_month != 'Z' else year - 1
        if prev_year == -1: prev_year == 9
        return f'ES{prev_month}{prev_year}'

    @staticmethod
    def get_next_symbol(curr_future_symbol: str) -> str:
        '''
        >>> assert(EminiFuture.get_next_symbol('ESZ8') == 'ESH9')
        '''
        month = curr_future_symbol[2]
        year = int(curr_future_symbol[3])
        next_month = {'Z': 'H', 'H': 'M', 'M': 'U', 'U': 'Z'}[month]
        next_year = year if next_month != 'H' else year + 1
        if next_year == 10: next_year = 0
        return f'ES{next_month}{next_year}'
    
    @staticmethod
    def get_expiry(fut_symbol: str) -> np.datetime64:
        '''
        >>> assert(EminiFuture.get_expiry('ESH8') == np.datetime64('2018-03-16T08:30'))
        '''
        month_str = fut_symbol[-2: -1]
        year_str = fut_symbol[-1:]
        
        month = future_code_to_month_number(month_str)
        assert(isinstance(month, int))
        year = int(year_str)
        year_base = 2020 if year < 5 else 2010
        year = year_base + int(year_str)
        expiry_date = EminiFuture.calendar.third_friday_of_month(month, year).astype(datetime.date)
        return np.datetime64(expiry_date) + np.timedelta64(8 * 60 + 30, 'm')
    

class EminiOption:
    
    calendar = Calendar.get_calendar(Calendar.NYSE)

    @staticmethod
    def decode_symbol(name: str) -> Tuple[weekday, int, int, int]:
        '''
        >>> EminiOption.decode_symbol('E1AF8')
        (MO, 2018, 1, 1)
        '''
        if re.match('EW[1-4].[0-9]', name):  # Friday
            year = int('201' + name[-1:])
            if year in [2010, 2011]: year += 10
            week = int(name[2:3])
            month = future_code_to_month_number(name[3:4])
            return rd.FR, year, month, week
        if re.match('E[1-5]A.[0-9]', name):  # Monday
            year = int('201' + name[-1:])
            if year in [2010, 2011]: year += 10
            week = int(name[1:2])
            month = future_code_to_month_number(name[3:4])
            return rd.MO, year, month, week
        if re.match('E[1-5]C.[0-9]', name):  # Wednesday
            year = int('201' + name[-1:])
            if year in [2010, 2011]: year += 10
            week = int(name[1:2])
            month = future_code_to_month_number(name[3:4])
            return rd.WE, year, month, week
        if re.match('EW[A-Z][0-9]', name):  # End of month
            year = int('201' + name[-1:])
            if year in [2010, 2011]: year += 10
            week = -1
            month = future_code_to_month_number(name[2:3])
            return rd.WE, year, month, week
        else:
            raise Exception(f'could not decode: {name}')
            
    @staticmethod
    def get_expiry(symbol: str) -> np.datetime64:
        '''
        >>> EminiOption.get_expiry('EW2Z5')
        numpy.datetime64('2015-12-11T15:00')
        >>> EminiOption.get_expiry('E3AF7')
        numpy.datetime64('2017-01-17T15:00')
        >>> EminiOption.get_expiry('EWF0')
        numpy.datetime64('2020-01-31T15:00')
        '''
        assert ':' not in symbol, f'{symbol} contains: pass in option root instead'
        weekday, year, month, week = EminiOption.decode_symbol(symbol)
        expiry_ = get_date_from_weekday(weekday.weekday, year, month, week)
        if weekday in [rd.WE, rd.FR]:
            expiry = EminiOption.calendar.add_trading_days(expiry_, num_days=0, roll='backward')
        else:
            expiry = EminiOption.calendar.add_trading_days(expiry_, num_days=0, roll='forward')
        # Option expirations changed on 9/20/2015 from 3:15 to 3 pm - 
        # See https://www.cmegroup.com/market-regulation/files/15-384.pdf
        expiry += np.where(expiry < np.datetime64('2015-09-20'), np.timedelta64(15 * 60 + 15, 'm'), np.timedelta64(15, 'h'))
        assert isinstance(expiry, np.datetime64)
        return expiry
       

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
