import requests
import pandas as pd

# ── CONFIG ────────────────────────────────────────────────────────────────────
SHOP_URL = "https://www.peepultree.world"  # Replace with target store URL

def fetch_all_products(shop_url):
    products_list = []
    page = 1

    while True:
        url = f"{shop_url}/products.json?limit=250&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            break

        data = response.json().get("products", [])

        if not data:
            break

        for product in data:
            title = product["title"]

            # ── Collect ALL image URLs for this product ────────────────────
            images = product.get("images", [])
            all_photo_urls = " | ".join([img["src"] for img in images])
            # URLs are separated by " | " so the CSV stays readable
            # Example: "https://cdn.../img1.jpg | https://cdn.../img2.jpg"

            if not all_photo_urls:
                all_photo_urls = "No images"

            # ── Each variant gets its own row ──────────────────────────────
            for variant in product["variants"]:
                products_list.append({
                    "Product Name" : title,
                    "Variant"      : variant["title"],
                    "Price"        : float(variant["price"]),
                    "Inventory"    : variant.get("inventory_quantity", "N/A"),
                    "Product ID"   : variant["id"],
                    "All Photos"   : all_photo_urls   # All URLs in one cell
                })

        print(f"Fetched page {page} — {len(data)} products")
        page += 1

    return products_list


def save_to_csv(products_list):
    df = pd.DataFrame(products_list)
    df.index += 1
    df.to_csv("products.csv", index_label="Row")
    print(f"\n✅ Saved {len(products_list)} products to products.csv")
    print("📸 All photo URLs saved in the 'All Photos' column, separated by ' | '")


if __name__ == "__main__":
    print("Fetching products...")
    products = fetch_all_products(SHOP_URL)
    save_to_csv(products)
