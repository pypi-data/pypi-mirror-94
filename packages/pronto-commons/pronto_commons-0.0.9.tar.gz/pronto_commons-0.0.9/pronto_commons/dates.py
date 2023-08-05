import datetime
from warnings import warn

try:
    import pytz
except ImportError:
    warn("pytz is not found and it is used in some methods inside this library", ImportWarning)


def get_iso_week_day(date: datetime.datetime, timezone: str) -> int:
    """ Function to return the iso weekday
        0 = Sunday
        1 = Monday
        2 = Tuesday
        3 = Wednesday
        4 = Thursday
        5 = Friday
        6 = Saturday
    """
    pst = pytz.timezone(timezone)
    return pst.fromutc(date).isoweekday() % 7



def datetime_with_timezone(_datetime: datetime.datetime, timezone: str) -> datetime.datetime:
    pst = pytz.timezone(timezone)
    return pst.fromutc(_datetime)


def date_to_datetime(date: datetime.date) -> datetime.datetime:
    return datetime.datetime(date.year, date.month, date.day, 0, 0, 0)



def local_date_to_utc(date: datetime.date, timezone: str):
    return (
        pytz.timezone(timezone)
        .localize(datetime.datetime(date.year, date.month, date.day))
        .astimezone(pytz.utc)
    )

