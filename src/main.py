from tqdm import tqdm
from scraper.fragment_requests import request_floor_page, request_sold_page, request_number_page
from time import sleep

from parser.html_parser import (
    parse_sale_html,
    parse_sold_html,
    parse_sold_number_page_and_add_owner,
    parse_sale_number_page_and_add_owner
)
from db.database import Database


def main():
    db = Database('my_database.db')

    while True:

        floor_items = parse_sale_html(request_floor_page())
        sold_items = parse_sold_html(request_sold_page())

        for item in tqdm(floor_items):
            updated_item = parse_sale_number_page_and_add_owner(
                item, request_number_page(item.link))

            record = updated_item.to_tuple()
            db.insert_sale_number_record(record)

        for item in tqdm(sold_items):
            updated_item = parse_sold_number_page_and_add_owner(
                item, request_number_page(item.link))

            record = updated_item.to_tuple()

            if not db.insert_sold_number_record(record):
                break

        sleep(60)


if __name__ == '__main__':
    main()
