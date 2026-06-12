import requests
import pandas as pd
import os
import re

# ── CONFIG ────────────────────────────────────────────────────────────────────
CSV_FILE    = "products.csv"       # Your product CSV
OUTPUT_DIR  = "product_images"     # Folder where images will be saved

def sanitise_name(name):
    """
    Removes special characters from product names so they
    can be safely used as folder names on any OS.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def download_images_for_rows(row_numbers):
    """
    Reads the CSV, filters chosen rows, and downloads
    all photos for each product into its own subfolder.
    """
    df = pd.read_csv(CSV_FILE, index_col="Row")

    # Validate row numbers
    valid_rows = [r for r in row_numbers if r in df.index]
    invalid_rows = [r for r in row_numbers if r not in df.index]

    if invalid_rows:
        print(f"⚠️  Skipping invalid rows: {invalid_rows}")

    if not valid_rows:
        print("❌ No valid rows found. Exiting.")
        return

    chosen = df.loc[valid_rows]

    # Create main output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_downloaded = 0
    total_failed     = 0

    for row, item in chosen.iterrows():
        product_name = sanitise_name(item["Product Name"])
        variant      = sanitise_name(str(item["Variant"]))
        photo_urls   = item["All Photos"]

        if pd.isna(photo_urls) or photo_urls == "No images":
            print(f"\n⚠️  Row {row} — {product_name} ({variant}): No images found, skipping.")
            continue

        # Split the " | " separated URLs back into a list
        urls = [url.strip() for url in photo_urls.split("|")]

        # Create a subfolder per product variant
        # e.g. product_images/Nike Air Max/Size 9/
        folder = os.path.join(OUTPUT_DIR, product_name, variant)
        os.makedirs(folder, exist_ok=True)

        print(f"\n📦 Row {row} — {product_name} ({variant}): {len(urls)} image(s)")

        for i, url in enumerate(urls, start=1):
            # Derive a clean filename from the URL
            # e.g. https://cdn.shopify.com/.../image.jpg → image.jpg
            filename  = url.split("?")[0].split("/")[-1]   # Strip query params
            save_path = os.path.join(folder, filename)

            # Skip if already downloaded
            if os.path.exists(save_path):
                print(f"   ⏭️  [{i}/{len(urls)}] Already exists — {filename}")
                continue

            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    print(f"   ✅ [{i}/{len(urls)}] Downloaded — {filename}")
                    total_downloaded += 1
                else:
                    print(f"   ❌ [{i}/{len(urls)}] Failed (HTTP {response.status_code}) — {url}")
                    total_failed += 1
            except requests.exceptions.RequestException as e:
                print(f"   ❌ [{i}/{len(urls)}] Error — {e}")
                total_failed += 1

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 50)
    print(f"✅ Downloaded : {total_downloaded} image(s)")
    print(f"❌ Failed     : {total_failed} image(s)")
    print(f"📁 Saved to   : {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    print("Enter row numbers to download images for (from products.csv)")
    print("Example: 1 4 7 12")
    print("Type 'all' to download images for every product\n")

    user_input = input("Row numbers: ").strip()

    if user_input.lower() == "all":
        df = pd.read_csv(CSV_FILE, index_col="Row")
        row_numbers = list(df.index)
    else:
        row_numbers = [int(r) for r in user_input.split()]

    download_images_for_rows(row_numbers)
