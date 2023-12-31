# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/economic-analysis-carb-allowance-prices.ipynb.

# %% auto 0
__all__ = ['clean_price', 'project_future_prices', 'visualize_scenarios_with_bands', 'interactive_visualization']

# %% ../nbs/economic-analysis-carb-allowance-prices.ipynb 6
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact, FloatSlider
import requests
from io import StringIO

# %% ../nbs/economic-analysis-carb-allowance-prices.ipynb 7
# Data cleaning and projection functions
def clean_price(price):
    """Convert price string to a float."""
    return float(price.replace('$', '').replace(',', '').strip())

def project_future_prices(dataframe, increase_rate, inflation_rate, years=10):
    """Project future auction reserve prices based on increase rate and inflation rate."""
    latest_price = dataframe['Auction Reserve Price'].iloc[-1]
    projected_years = [dataframe['Year'].iloc[-1] + i for i in range(1, years + 1)]
    projected_prices = [latest_price * ((1 + increase_rate) ** i) * ((1 + inflation_rate) ** i) for i in range(1, years + 1)]
    return pd.DataFrame({'Year': projected_years, 'Projected Auction Reserve Price': projected_prices})

# %% ../nbs/economic-analysis-carb-allowance-prices.ipynb 8
# Visualization function with color customization, bands, and logo
def visualize_scenarios_with_bands(historical, projected, title_color, line_color, band_color, background_color):
    sns.set(style='white', rc={'axes.facecolor': background_color})
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot historical data
    ax.plot(historical['Year'], historical['Auction Reserve Price'], label='Historical', marker='o', color=line_color)

    # Plot projected data for base case
    ax.plot(projected['Year'], projected['Projected Auction Reserve Price'], label='Projected', linestyle='--', marker='x', color=line_color)

    # Create bands for upper and lower bounds
    upper_bound = [price * 1.05 for price in projected['Projected Auction Reserve Price']]
    lower_bound = [price * 0.95 for price in projected['Projected Auction Reserve Price']]

    # Fill between the upper and lower bounds
    ax.fill_between(projected['Year'], lower_bound, upper_bound, color=band_color, alpha=0.2)

    # Customize the title and labels
    plt.title('Historical and Projected Auction Reserve Prices', color=title_color)
    plt.xlabel('Year')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()

# %% ../nbs/economic-analysis-carb-allowance-prices.ipynb 10
# Interactive visualization function
def interactive_visualization(increase_rate=0.05, inflation_rate=0.02):
    # Assuming the file is named 'November_09_2023_nc-allowance_prices.csv' and is uploaded to Colab
    file_path = 'November_09_2023_nc-allowance_prices.csv'
    allowance_prices = pd.read_csv(download_directory+'/'+file_path)

    # Data cleaning
    allowance_prices[['Quarter', 'Year']] = allowance_prices['Quarter Year'].str.split(' ', expand=True)
    allowance_prices['Year'] = allowance_prices['Year'].astype(int)
    allowance_prices['Auction Reserve Price'] = allowance_prices['Auction Reserve Price'].apply(clean_price)

    # Project future prices
    projected_prices_df = project_future_prices(allowance_prices, increase_rate, inflation_rate)

    # Define colors using provided RGB values converted to hex
    title_color = '#000b10'  # Dark shade of blue
    line_color = '#294646'   # Moderate greenish-gray
    band_color = '#2c4747'   # Medium gray with a slight purple tint
    background_color = '#f5f5f5'  # Off white

    # Visualize the scenarios with custom colors and bands
    visualize_scenarios_with_bands(allowance_prices, projected_prices_df, title_color, line_color, band_color, background_color)

# %% ../nbs/economic-analysis-carb-allowance-prices.ipynb 11
# Set up the interactive widget
interact(interactive_visualization,
         increase_rate=FloatSlider(value=0.05, min=0, max=0.15, step=0.01, description='Increase Rate:'),
         inflation_rate=FloatSlider(value=0.02, min=-0.05, max=0.1, step=0.01, description='Inflation Rate:'))
