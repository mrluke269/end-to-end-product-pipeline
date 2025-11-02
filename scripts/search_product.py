#!/usr/bin/env python3
import requests
import json
from config import RAPIDAPI_KEY, RAPIDAPI_HOST
from pathlib import Path  # <-- Import Path


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

# Ensure the 'data' directory exists
DATA_DIR.mkdir(exist_ok=True)

# Define the full path for the output file
output_file_path = DATA_DIR / 'asins_to_fetch.json'


# Search for products with query "dog food"
response = requests.get(f'https://{RAPIDAPI_HOST}/search?query=dog food&page=1&country=US&sort_by=RELEVANCE&product_condition=ALL&is_prime=false&deals_and_discounts=NONE', 
    headers={
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    })
print(response.status_code)
print('Search query used: dog food')

# Get the JSON response
search_result = response.json()

# Extract the list of products
products_list = search_result['data']['products']

# Get ASINs of the first 10 products
asin_list = []
for p in products_list[:10]:
    asin = p['asin']
    asin_list.append(asin)

# Save ASINs to the relative file path
with open(output_file_path, 'w') as f:  
    f.write(json.dumps(asin_list, indent=2))
    print(f'ASINs saved to {output_file_path}') 