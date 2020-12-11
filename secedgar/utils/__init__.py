import datetime
import errno
import os
import requests

from secedgar.utils.cik_map import get_cik_map  # noqa


def sanitize_date(date):
    """Sanitizes date to be in acceptable format for EDGAR.

    Args:
        date (Union[datetime.datetime, str]): Date to be sanitized for request.

    Returns:
        date (str): Properly formatted date in 'YYYYMMDD' format.

    Raises:
        TypeError: If date is not in format YYYYMMDD as str or int.
    """
    if isinstance(date, datetime.datetime):
        return date.strftime("%Y%m%d")
    elif isinstance(date, str):
        if len(date) != 8:
            raise TypeError('Date must be of the form YYYYMMDD')
    elif isinstance(date, int):
        if date < 10 ** 7 or date > 10 ** 8:
            raise TypeError('Date must be of the form YYYYMMDD')
    return date


def make_path(path, **kwargs):
    """Make directory based on filing info.

    Args:
        path (str): Path to be made if it doesn't exist.

    Raises:
        OSError: If there is a problem making the path.

    Returns:
        None
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path, **kwargs)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise OSError


async def download_link_to_path(link, path):
    """Downloads a link to the specified path

    Args:
        link (str): Link to download
        path (str): Full file path

    Returns:
        None
    """
    data = requests.get(link).text
    make_path(os.path.dirname(path))
    with open(path, "w") as f:
        f.write(data)


def get_quarter(date):
    """Get quarter that corresponds with date.

    Args:
        date ([datetime.datetime]): Datetime object to get quarter for.
    """
    return (date.month - 1) // 3 + 1