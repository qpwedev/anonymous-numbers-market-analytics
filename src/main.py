import asyncio
from tqdm import tqdm
from scraper.fragment_requests import request_floor_page, request_sold_page, request_number_page
from time import strftime

from data_visualization.plotting_tools import plot_floor

from parser.html_parser import (
    parse_sale_html,
    parse_sold_html,
    parse_sold_number_page_and_add_owner,
    parse_sale_number_page_and_add_owner
)
from db.database import Database
from telegram_bot.bot import send_photo
from text_generation.telegram_post_text import records_to_text
from utils import async_retry


@async_retry(
    retry_on_exception=lambda e: isinstance(e, (Exception,)),
    wait_fixed=30,
)
async def main():
    db = Database('my_database.db')
    counter = 0

    while True:
        floor_items = parse_sale_html(request_floor_page())
        sold_items = parse_sold_html(request_sold_page())

        for item in tqdm(floor_items):
            updated_item = parse_sale_number_page_and_add_owner(
                item, request_number_page(item.link))

            record = updated_item.to_tuple()
            db.insert_sale_number_record(record)

        # plotting and telegram sending every 5 minutes
        if counter % 10 == 0:
            plot_floor(floor_items)
            await send_photo('nft_plot.png', records_to_text(floor_items))

        for item in tqdm(sold_items):
            updated_item = parse_sold_number_page_and_add_owner(
                item, request_number_page(item.link))

            record = updated_item.to_tuple()

            if not db.insert_sold_number_record(record):
                break

        counter += 1
        await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
