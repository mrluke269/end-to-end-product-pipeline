# !/usr/bin/env python3
import requests
import json
from config import RAPIDAPI_KEY, RAPIDAPI_HOST
from pathlib import Path  # <-- Import Path

# --- Start of Fix ---
# Define paths relative to this script
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DETAILS_DIR = DATA_DIR / 'product_details'

# Ensure the directories exist
DETAILS_DIR.mkdir(parents=True, exist_ok=True)

# Define file paths
asin_file_path = DATA_DIR / 'asins_to_fetch.json'
combined_file_path = DETAILS_DIR / 'combined_products.json'
# --- End of Fix ---


# Read ASINs from relative JSON file
with open(asin_file_path, 'r') as f:  # <-- Use the new path variable
    asin_list = json.load(f)

print(f"Starting to fetch {len(asin_list)} products...")
# Fetch and save product details for each ASIN
for asin in asin_list:
    try:
        response = requests.get(f'https://{RAPIDAPI_HOST}/product-details?asin={asin}&country=US', 
    headers={
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    })
        response.raise_for_status()
        product_data = response.json()
        
        # Define the output path for this specific ASIN
        product_output_path = DETAILS_DIR / f'{asin}.json' # 
        
        with open(product_output_path, 'w') as f:
            json.dump(product_data, f, indent=2)
        print(f"✅ Saved {asin} to {product_output_path}") 
        
    except Exception as e:
        print(f"❌ Failed to fetch/save {asin}: {e}")
print("Done fetching product details!")

# Combine all product details into a single JSON file
all_products = []
for asin in asin_list:
    product_file = DETAILS_DIR / f'{asin}.json' 
    with open(product_file, 'r') as f:
        product_data = json.load(f)
        all_products.append(product_data)

with open(combined_file_path, 'w') as f: 
    json.dump(all_products, f, indent=2)
print(f"✅ Combined product details saved to {combined_file_path}")