import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from models.number_records import SaleNumberRecord

plt.style.use('ggplot')


def plot_floor(records):

    # Create a default dictionary to hold counts for each owner at each price point
    price_to_owner_counts = defaultdict(lambda: defaultdict(int))

    # Iterate over SaleNumberRecord list to fill the dictionary
    for record in records:
        price_to_owner_counts[record.price][record.owner] += 1

    # Prepare data for the stacked bar plot
    prices = sorted(price_to_owner_counts.keys())
    total_counts_per_owner = defaultdict(int)

    for price in prices:
        for owner, count in price_to_owner_counts[price].items():
            total_counts_per_owner[owner] += count

    # Sorting owners by total counts
    owners = sorted(total_counts_per_owner.keys(),
                    key=lambda x: total_counts_per_owner[x], reverse=True)

    # Generate list of lists for plot data
    plot_data = []
    for owner in owners:
        owner_data = []
        for price in prices:
            owner_data.append(price_to_owner_counts[price][owner])
        plot_data.append(owner_data)

    # Sorting plot_data and owners based on the total counts (sum of each sublist in plot_data)
    plot_data, owners = zip(
        *sorted(zip(plot_data, owners), key=lambda x: sum(x[0]), reverse=True))

    # Create stacked bar plot
    fig, ax = plt.subplots(figsize=(20, 10))

    # Increase font size for readability
    plt.rcParams.update({'font.size': 14})

    # Using numpy's `cumsum` function helps to stack the bars
    cumulative_data = np.cumsum(plot_data, axis=0)
    for i, owner_data in enumerate(plot_data):
        ax.bar(prices, owner_data, bottom=(
            cumulative_data[i-1] if i > 0 else None), label=owners[i])

    # Other plot settings
    ax.set_xlabel('Price')
    ax.set_ylabel('Number of NFTs')
    ax.set_title(
        'Supply on Anonymous Numbers\nVisit Telegram: @numbersupply. Powered by qpwe 👾\n')

    # Rotate x-axis labels by 90 degrees
    plt.xticks(rotation=90)

    # Adjust margins to eliminate white spaces around the plot
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.15)

    # Save the plot as a PNG file
    plt.savefig('nft_plot.png', dpi=300, bbox_inches='tight')
