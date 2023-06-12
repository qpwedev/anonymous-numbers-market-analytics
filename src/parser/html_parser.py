"""
Module to parse sales-related HTML data using BeautifulSoup.
"""

from bs4 import BeautifulSoup
from models.number_records import SaleNumberRecord, SoldNumberRecord
from typing import Optional, List


def parse_sale_html(html_content) -> List[SaleNumberRecord]:
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select(
        '#aj_content > main > section.tm-section.clearfix.js-search-results > div.tm-table-wrap > table > tbody > tr')

    records = []
    for element in elements:
        link_element = element.select_one('td > a')
        link = link_element['href'] if link_element else None

        number_element = element.select_one('.tm-value')
        number = number_element.text.strip() if number_element else None

        status_element = element.select_one('.tm-status-avail')
        status = status_element.text.strip() if status_element else None

        price_element = element.select_one('td.thin-last-col > a > .tm-value')
        price = price_element.text.strip() if price_element else None

        time_element = element.select_one('.tm-timer > time')
        time_left = time_element.text.strip() if time_element else None

        record = SaleNumberRecord(link, number, status, price, time_left)
        records.append(record)

    return records


def parse_sold_html(html_content) -> List[SoldNumberRecord]:
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select(
        '#aj_content > main > section.tm-section.clearfix.js-search-results > div.tm-table-wrap > table > tbody > tr')

    records = []
    for element in elements:
        link_element = element.select_one('td > a')
        link = link_element['href'] if link_element else None

        number_element = element.select_one('.tm-value')
        number = number_element.text.strip() if number_element else None

        status_element = element.select_one('.tm-status-unavail')
        status = status_element.text.strip() if status_element else None

        price_element = element.select_one('td.thin-last-col > a > .tm-value')
        price = price_element.text.strip() if price_element else None

        time_element = element.select_one(
            'td.wide-last-col > a > .table-cell-desc > time')
        sold_time = time_element.text.strip() if time_element else None

        record = SoldNumberRecord(link, number, status, price, sold_time)
        records.append(record)

    return records


def parse_sold_number_page_and_add_owner(record, html_content) -> SoldNumberRecord:
    soup = BeautifulSoup(html_content, 'html.parser')

    # Parse Sale Price
    sale_price_element = soup.select_one('.tm-section-bid-info .tm-value')
    record.sale_price = sale_price_element.text.strip() if sale_price_element else None

    # Parse Owner
    owner_element = soup.select_one('.tm-section-bid-info .tm-wallet')
    record.owner = owner_element['href'] if owner_element else None

    return record


def parse_sale_number_page_and_add_owner(record: SaleNumberRecord, html_content: str) -> SaleNumberRecord:
    """
    Parses the HTML content and adds the owner attribute to the SaleNumberRecord instance.

    :param record: The SaleNumberRecord instance to be updated.
    :param html_content: The HTML content to be parsed.
    :return: The updated SaleNumberRecord instance.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Select the first row of the ownership history table
    first_row = soup.select_one(
        '#aj_content > main > section.tm-section.clearfix > div.tm-table-wrap > table > tbody > tr:nth-child(1)')

    if first_row is not None:
        # Select the 'tm-wallet' element within the first row
        owner_element = first_row.select_one('.tm-wallet')
        if owner_element:
            # Update the owner attribute of the record
            record.owner = owner_element.get('href')

    return record
