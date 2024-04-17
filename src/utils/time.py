"""Time"""
from datetime import datetime

import pytz

from src.configs.constants import MasterConstants


def get_current_datetime(
    time_zone: str = MasterConstants.DEFAULT_TIME_ZONE, return_string=True, is_date_only=False,
    time_format: str = MasterConstants.DEFAULT_DATETIME_FORMAT
):
    """Get current time according to timezone"""
    server_timezone = pytz.timezone(time_zone)
    if return_string is True:
        if is_date_only is False:
            return datetime.now(server_timezone).strftime(time_format)
        return datetime.now(server_timezone).strftime(
            MasterConstants.DEFAULT_DATE_FORMAT
        )
    else:
        return datetime.now(server_timezone).replace(microsecond=0, tzinfo=None)