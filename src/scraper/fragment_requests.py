import requests
from tenacity import retry, wait_exponential, stop_after_attempt


FLOOR_PAGE_PARAMS = {
    'sort': 'price_asc',
    'filter': 'sale',
}

SOLD_PAGE_PARAMS = {
    'sort': 'listed',
    'filter': 'sold',
}


@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
def request_fragment_page(link, params):
    response = requests.get(
        'https://fragment.com/' + link,
        params=params,
        timeout=5
    )

    response.raise_for_status()

    return response.text


def request_sold_page():
    return request_fragment_page(
        'numbers',
        SOLD_PAGE_PARAMS
    )


def request_floor_page():
    return request_fragment_page(
        'numbers',
        FLOOR_PAGE_PARAMS
    )


def request_number_page(link):

    return request_fragment_page(link, {})
