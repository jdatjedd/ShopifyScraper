import requests
import pandas as pd
from datetime import datetime

SHOP_URL = "https://yourstore.myshopify.com"  # Same store URL as fetch.py

def get_current_price(product_id):
    """
    Fetches the latest price of a variant directly from Shopify's API
    using the product variant ID saved in the CSV.
    """
    url = f"{SHOP_URL}/products.json?limit=250"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    for product in response.json().get("products", []):
        for variant in product["variants"]:
            if variant["id"] == product_id:
                return float(variant["price"])
    return None


def track_prices(row_numbers):
    """
    Loads products.csv, filters chosen rows, checks current prices,
    and reports any changes.
    """
    df = pd.read_csv("products.csv", index_col="Row")

    chosen = df.loc[row_numbers]  # Filter only chosen rows

    # Save chosen items to tracked.csv on first run
    chosen.to_csv("tracked.csv")
    print(f"\nTracking {len(chosen)} item(s) — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"{'Row':<5} {'Product':<40} {'Saved Price':<15} {'Current Price':<15} {'Change'}")
    print("-" * 90)

    for row, item in chosen.iterrows():
        saved_price   = item["Price"]
        product_id    = item["Product ID"]
        current_price = get_current_price(int(product_id))

        if current_price is None:
            print(f"{row:<5} {item['Product Name']:<40} ₹{saved_price:<14} Could not fetch")
            continue

        # Calculate change
        change = current_price - saved_price
        if change < 0:
            status = f"🟢 DROP  ₹{abs(change):.2f}"
        elif change > 0:
            status = f"🔴 RISE  ₹{change:.2f}"
        else:
            status = "⚪ No change"

        print(f"{row:<5} {item['Product Name']:<40} ₹{saved_price:<14} ₹{current_price:<14} {status}")


if __name__ == "__main__":
    print("Enter row numbers to track (from products.csv)")
    print("Example: 1 4 7 12")
    user_input = input("Row numbers: ").strip().split()
    row_numbers = [int(r) for r in user_input]
    track_prices(row_numbers)
