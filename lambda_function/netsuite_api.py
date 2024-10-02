import os
import requests
import json
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NetSuite API credentials loaded from environment variables
NETSUITE_ACCOUNT_ID = os.getenv("NETSUITE_ACCOUNT_ID")
NETSUITE_CONSUMER_KEY = os.getenv("NETSUITE_CONSUMER_KEY")
NETSUITE_CONSUMER_SECRET = os.getenv("NETSUITE_CONSUMER_SECRET")
NETSUITE_TOKEN_ID = os.getenv("NETSUITE_TOKEN_ID")
NETSUITE_TOKEN_SECRET = os.getenv("NETSUITE_TOKEN_SECRET")

# NetSuite REST API Base URL
NETSUITE_REST_BASE_URL = f"https://{NETSUITE_ACCOUNT_ID}.suitetalk.api.netsuite.com/services/rest/record/v1"

# Utility function for generating OAuth 1.0 headers (This needs to be customized)
def generate_oauth_headers():
    """Placeholder function to generate OAuth headers. Customize this function for your authentication."""
    # Replace with your OAuth header generation logic
    return {
        "Authorization": f"OAuth oauth_consumer_key={NETSUITE_CONSUMER_KEY}, oauth_token={NETSUITE_TOKEN_ID}, oauth_signature_method='HMAC-SHA256', oauth_timestamp='timestamp', oauth_nonce='nonce', oauth_version='1.0', oauth_signature='signature'"
    }

def get_products():
    """Fetch a list of products from NetSuite."""
    url = f"{NETSUITE_REST_BASE_URL}/inventoryItem"
    headers = generate_oauth_headers()
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            products = response.json()
            logger.info("Successfully fetched products from NetSuite.")
            return products.get("items", [])  # Adjust based on NetSuite's response format
        else:
            logger.error(f"Error fetching products: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while fetching products: {e}")
        return None

def update_product_price(product_id, new_price):
    """Update the price of a product in NetSuite."""
    url = f"{NETSUITE_REST_BASE_URL}/inventoryItem/{product_id}"
    headers = generate_oauth_headers()
    headers["Content-Type"] = "application/json"

    data = {
        "itemId": product_id,  # Adjust field names based on NetSuite's schema
        "basePrice": new_price
    }

    try:
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f"Successfully updated product ID {product_id} to new price: {new_price}")
        else:
            logger.error(f"Error updating price for product ID {product_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"An error occurred while updating price: {e}")

def print_products(products):
    """Print the IDs and names of products from NetSuite."""
    if products:
        for product in products:
            logger.info(f"ID: {product['id']}, Name: {product['itemName']}")
    else:
        logger.info("No products to display.")

# Testing the functions locally
if __name__ == "__main__":
    # Fetch and print products
    products = get_products()
    if products:
        print_products(products)
        
    # Example price update (replace with actual product ID and price)
    update_product_price("12345", 99.99)
