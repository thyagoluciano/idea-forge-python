import datetime
from datetime import datetime, timedelta, timezone


def get_utc_timestamp(date):
    if isinstance(date, float):
        date = datetime.fromtimestamp(date, tz=timezone.utc)
    return int(date.timestamp())


def get_start_end_timestamps(days_ago):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_ago)

    return get_utc_timestamp(start_date), get_utc_timestamp(end_date)
