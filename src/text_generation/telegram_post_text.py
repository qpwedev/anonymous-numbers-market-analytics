from collections import defaultdict
from models.number_records import SaleNumberRecord


def records_to_text(records):
    # Initial text with floor price
    text = f'<b><a href="https://fragment.com/{records[0].link}">Floor: {str(records[0].price)}</a></b>\n\n'

    # Group records by price
    records_by_price = defaultdict(list)
    for record in records:
        records_by_price[record.price].append(record)

    # Generate a summary for each price point
    summaries = []
    for price, records_at_price in sorted(records_by_price.items()):
        new_line = f'{price}: {len(records_at_price)}'

        # If adding the new line exceeds the limit, break the loop
        if len(text) + len(new_line) + 1 > 2048:  # +1 for ' '
            break

        summaries.append(new_line)

    text += ' | '.join(summaries)

    # Add footer text, if there's enough space left
    footer = """Chat 👉🏼 <b>@HoldNumbers</b>"""

    # Truncate the main text if necessary to make room for the footer
    if len(text) + len(footer) + 2 > 2048:  # +2 for '\n\n'
        text = text[:2048 - len(footer) - 2] + '\n\n' + footer
    else:
        text += '\n\n' + footer

    return text
