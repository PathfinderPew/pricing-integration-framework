import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Zoey API credentials loaded from environment variables
ZOEY_API_URL = os.getenv("ZOEY_API_URL", "https://api.zoey.com")  # Default to common Zoey API URL if not specified
ZOEY_CLIENT_ID = os.getenv("ZOEY_CLIENT_ID")
ZOEY_CLIENT_SECRET = os.getenv("ZOEY_CLIENT_SECRET")
ZOEY_ACCESS_TOKEN = os.getenv("ZOEY_ACCESS_TOKEN")  # Use the stored access token for authentication


def get_access_token():
    """Fetch a new access token from Zoey using client credentials (if required)."""
    url = f"{ZOEY_API_URL}/oauth/token"
    data = {
        "client_id": ZOEY_CLIENT_ID,
        "client_secret": ZOEY_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            logger.info("Successfully fetched Zoey access token.")
            return access_token
        else:
            logger.error(f"Failed to get access token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while fetching access token: {e}")
        return None


def get_products():
    """Fetch a list of products from Zoey."""
    url = f"{ZOEY_API_URL}/v1/products"
    headers = {"Authorization": f"Bearer {ZOEY_ACCESS_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            products = response.json().get("data", [])
            logger.info("Successfully fetched products from Zoey.")
            return products
        else:
            logger.error(f"Error fetching products: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while fetching products from Zoey: {e}")
        return None


def update_product_price(product_id, new_price):
    """Update the price of a product in Zoey."""
    url = f"{ZOEY_API_URL}/v1/products/{product_id}"
    headers = {"Authorization": f"Bearer {ZOEY_ACCESS_TOKEN}"}
    data = {
        "data": {
            "id": product_id,
            "type": "product",
            "attributes": {
                "price": new_price
            }
        }
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
    """Print the IDs and names of products from Zoey."""
    if products:
        for product in products:
            logger.info(f"ID: {product['id']}, Name: {product['attributes']['name']}")
    else:
        logger.info("No products to display.")


# For testing locally
if __name__ == "__main__":
    # Check if access token is missing and fetch a new one if needed
    if not ZOEY_ACCESS_TOKEN:
        ZOEY_ACCESS_TOKEN = get_access_token()

    # Fetch and print products
    products = get_products()
    if products:
        print_products(products)

    # Example price update (replace with a valid product ID and price)
    update_product_price("12345", 99.99)  # Example product ID and new price
