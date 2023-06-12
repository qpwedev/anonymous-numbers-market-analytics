"""
Module is responsible for requesting different pages from fragment.com. 
It includes functions to request the sold page, floor page, and individual number pages.
Each function uses the `request_fragment_page` function, which implements retry logic.
"""


from typing import Dict
import requests
from tenacity import retry, wait_exponential, stop_after_attempt

FLOOR_PAGE_PARAMS: Dict[str, str] = {
    'sort': 'price_asc',
    'filter': 'sale',
}

SOLD_PAGE_PARAMS: Dict[str, str] = {
    'sort': 'ending',
    'filter': 'sold',
}


@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
def request_fragment_page(link: str, params: Dict[str, str]) -> str:
    """
    Sends a GET request to the specified link at fragment.com with the provided parameters.

    Args:
        link (str): The specific page on fragment.com to request.
        params (Dict[str, str]): The parameters to include in the GET request.

    Returns:
        str: The response text of the GET request.

    Raises:
        HTTPError: If the GET request fails, it will be retried up to 5 times with exponential backoff.
    """
    response = requests.get(
        'https://fragment.com/' + link,
        params=params,
        timeout=5
    )

    response.raise_for_status()

    return response.text


def request_sold_page() -> str:
    """
    Requests the sold page from fragment.com.

    Returns:
        str: The response text of the GET request to the sold page.
    """
    return request_fragment_page(
        'numbers',
        SOLD_PAGE_PARAMS
    )


def request_floor_page() -> str:
    """
    Requests the floor page from fragment.com.

    Returns:
        str: The response text of the GET request to the floor page.
    """
    return request_fragment_page(
        'numbers',
        FLOOR_PAGE_PARAMS
    )


def request_number_page(link: str) -> str:
    """
    Requests a specific number page from fragment.com.

    Args:
        link (str): The specific number page to request.

    Returns:
        str: The response text of the GET request to the number page.
    """
    return request_fragment_page(link, {})
