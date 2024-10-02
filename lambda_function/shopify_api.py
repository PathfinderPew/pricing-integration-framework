import requests

API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
STORE_NAME = 'your_store_name'

def get_products():
    """Fetch products from the Shopify API."""
    url = f'https://{STORE_NAME}.myshopify.com/admin/api/2023-04/products.json'
    try:
        response = requests.get(url, auth=(API_KEY, API_SECRET))
        if response.status_code == 200:
            return response.json().get('products', [])
        else:
            print(f"Error fetching products: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching products: {e}")
        return None

def print_products(products):
    """Print the titles and IDs of products."""
    if products:
        for product in products:
            print(f"Title: {product['title']}, ID: {product['id']}")
    else:
        print("No products to display.")

def update_product_price(product_id, variant_id, new_price):
    """Update the price of a product variant."""
    url = f'https://{STORE_NAME}.myshopify.com/admin/api/2023-04/variants/{variant_id}.json'
    data = {
        "variant": {
            "id": variant_id,
            "price": new_price
        }
    }
    try:
        response = requests.put(url, json=data, auth=(API_KEY, API_SECRET))
        if response.status_code == 200:
            print(f"Updated product ID {product_id} variant ID {variant_id} to new price: {new_price}")
        else:
            print(f"Error updating price: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred while updating price: {e}")

def apply_discount(products, discount_percent):
    """Apply a discount to all products."""
    for product in products:
        for variant in product['variants']:
            original_price = float(variant['price'])
            discount_amount = original_price * (discount_percent / 100)
            new_price = original_price - discount_amount
            update_product_price(product['id'], variant['id'], f"{new_price:.2f}")

if __name__ == "__main__":
    # Main execution
    products = get_products()
    print_products(products)
