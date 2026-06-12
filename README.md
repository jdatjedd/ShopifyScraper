# 🛒 Shopify Product Tracker

A Python toolkit to fetch, monitor, and download product data from any public Shopify store — no API key required.

Track price changes, monitor inventory, and bulk-download product images all from the command line.

---

## ✨ Features

- 📋 Fetch complete product listings (name, variant, price, inventory, images)
- 💾 Save everything to a clean, organised CSV
- 📈 Track price changes on selected products across runs
- 🟢 Visual indicators for price drops, rises, and no change
- 📸 Bulk download all product images into organised folders
- ⏭️ Smart skip — won't re-download images that already exist
- 🌐 Works on any public Shopify store without an API key

---

## 📁 Project Structure

```
ShopifyTracker/
│
├── fetch.py              # Fetches all products and saves to CSV
├── tracker.py            # Checks current prices against saved prices
├── downloader.py         # Downloads product images from the CSV
│
├── products.csv          # Auto-generated — full product list
├── tracked.csv           # Auto-generated — your chosen tracked items
│
└── product_images/       # Auto-generated — downloaded images
    ├── Product Name/
    │   └── Variant/
    │       ├── image1.jpg
    │       └── image2.jpg
    └── ...
```

---

## ⚙️ Installation

**Requirements:** Python 3.8+

```bash
pip install requests pandas
```

---

## 🚀 How to Use

### Step 1 — Fetch all products

Set your store URL in `fetch.py`:

```python
SHOP_URL = "https://yourstore.myshopify.com"
```

Then run:

```bash
python fetch.py
```

This generates `products.csv` with every product listed on the store.

---

### Step 2 — Track prices

Open `products.csv` and note the **Row numbers** of items you want to monitor.

Set the same store URL in `tracker.py`, then run:

```bash
python tracker.py
```

Enter your chosen row numbers when prompted:

```
Enter row numbers to track (from products.csv)
Example: 1 4 7 12
Row numbers: 2 5 9
```

---

### Step 3 — Download images *(optional)*

```bash
python downloader.py
```

Enter row numbers or type `all` to download every product's images:

```
Row numbers: all
```

Images are saved to `product_images/` organised by product and variant.

---

## 📊 Sample Output

### fetch.py
```
Fetching products...
Fetched page 1 — 250 products
Fetched page 2 — 143 products

✅ Saved 393 products to products.csv
📸 All photo URLs saved in the 'All Photos' column, separated by ' | '
```

### tracker.py
```
Tracking 3 item(s) — 2024-11-01 10:30:00

Row   Product                         Saved Price     Current Price   Change
------------------------------------------------------------------------------
2     Nike Air Max 90                 ₹4999           ₹4499           🟢 DROP  ₹500.00
5     Adidas Ultraboost 22            ₹6999           ₹6999           ⚪ No change
9     Puma RS-X                       ₹3499           ₹3799           🔴 RISE  ₹300.00
```

### downloader.py
```
📦 Row 2 — Nike Air Max 90 (Size 9): 3 image(s)
   ✅ [1/3] Downloaded — image1.jpg
   ✅ [2/3] Downloaded — image2.jpg
   ✅ [3/3] Downloaded — image3.jpg

──────────────────────────────────────────
✅ Downloaded : 3 image(s)
❌ Failed     : 0 image(s)
📁 Saved to   : /ShopifyTracker/product_images
```

---

## 🗂️ CSV Format

| Row | Product Name | Variant | Price | Inventory | Product ID | All Photos |
|-----|-------------|---------|-------|-----------|------------|------------|
| 1 | Nike Air Max | Size 9 | 4999 | 50 | 123456 | https://cdn/.../1.jpg \| https://cdn/.../2.jpg |
| 2 | Adidas Ultra | Size 10 | 6999 | 30 | 789012 | https://cdn/.../3.jpg |

> **All Photos** column stores multiple image URLs separated by ` | `  
> Copy any URL and paste into your browser to view the image directly.

---

## 🧠 Tech Stack

| Tool | Purpose |
|------|---------|
| [Requests](https://docs.python-requests.org/) | Fetching data from Shopify's JSON API |
| [pandas](https://pandas.pydata.org/) | Reading and writing CSV files |
| [os / re](https://docs.python.org/3/library/os.html) | Folder creation and filename sanitisation |
| Shopify `/products.json` | Public product data endpoint |

---

## ⚙️ Configuration

| Variable | File | Default | Description |
|----------|------|---------|-------------|
| `SHOP_URL` | `fetch.py`, `tracker.py` | — | Target Shopify store URL |
| `CSV_FILE` | `downloader.py` | `products.csv` | Path to your product CSV |
| `OUTPUT_DIR` | `downloader.py` | `product_images` | Folder to save downloaded images |

---

## ⚠️ Known Limitations

- Only works on Shopify stores that have **public product listings enabled**. Stores with password protection or restricted APIs will return a `403` or `404` error.
- Inventory quantity may show `N/A` if the store has hidden stock levels.
- Shopify's `/products.json` endpoint returns a maximum of **250 products per page** — the script handles pagination automatically.

---

## 💡 Possible Improvements

- 📧 Email alerts when a tracked price drops
- 📊 Price history graph using matplotlib
- 🗃️ SQLite database instead of CSV for larger stores
- 🌐 Flask web dashboard to manage tracked products
- ⏰ Scheduled auto-runs using the `schedule` library

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Pull requests are welcome! If you find a store where the scraper breaks or have an improvement in mind, feel free to open an issue.
