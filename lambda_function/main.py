import json
from .shopify_api import get_products as get_shopify_products, print_products as print_shopify_products, update_product_price as update_shopify_price
from .netsuite_api import get_products as get_netsuite_products, update_product_price as update_netsuite_price
from .zoey_api import get_products as get_zoey_products, update_product_price as update_zoey_price
from mock_data import mock_products  # Use mock data directly


# Mock function to fetch competitor prices (replace with actual scraping logic)
def fetch_competitor_prices():
    """Mock competitor prices. In a real scenario, you would scrape or use APIs to fetch competitor prices."""
    return {
        1: 9.50,  # Competitor price for Product 1 (lower than our price)
        2: 16.00  # Competitor price for Product 2 (higher than our price)
    }


def compare_and_update_prices(products, competitor_prices, update_function, platform_name="Shopify"):
    """Compare prices with competitor prices and update if necessary."""
    for product in products:
        product_id = product['id']
        for variant in product['variants']:
            variant_id = variant['id']
            current_price = float(variant['price'])
            competitor_price = competitor_prices.get(product_id, None)

            if competitor_price and competitor_price < current_price:
                print(f"Competitor price ({competitor_price}) is lower than {platform_name} price ({current_price}) for Product ID {product_id}. Updating price...")
                update_function(product_id, variant_id, f"{competitor_price:.2f}")
            else:
                print(f"{platform_name} price ({current_price}) is competitive or lower for Product ID {product_id}. No update needed.")


def lambda_handler(event, context):
    """AWS Lambda entry point."""

    # Determine which platform to use: mock, Shopify, NetSuite, or Zoey
    platform = event.get('platform', 'mock')  # Choose between 'mock', 'shopify', 'netsuite', or 'zoey'
    use_mock_data = platform == 'mock'
    competitor_prices = fetch_competitor_prices()  # Fetch competitor prices (replace with actual implementation)

    # Fetch products based on the specified platform
    if use_mock_data:
        products = mock_products['products']  # Use mock data for testing
        print("Using mock data:")
        print_shopify_products(products)  # Reusing print function for mock data
    elif platform == 'shopify':
        products = get_shopify_products()  # Fetch live products from Shopify
        if not products:
            return {
                'statusCode': 500,
                'body': json.dumps('Error fetching products from Shopify.')
            }
        print("Using live Shopify data:")
        print_shopify_products(products)
    elif platform == 'netsuite':
        products = get_netsuite_products()  # Fetch live products from NetSuite
        if not products:
            return {
                'statusCode': 500,
                'body': json.dumps('Error fetching products from NetSuite.')
            }
        print("Using live NetSuite data:")
        print_shopify_products(products)  # Reusing the same print function since structure is similar
    elif platform == 'zoey':
        products = get_zoey_products()  # Fetch live products from Zoey
        if not products:
            return {
                'statusCode': 500,
                'body': json.dumps('Error fetching products from Zoey.')
            }
        print("Using live Zoey data:")
        print_shopify_products(products)  # Reusing the same print function for consistency

    # Compare and update prices based on competitor data
    if platform == 'shopify':
        compare_and_update_prices(products, competitor_prices, update_shopify_price, platform_name="Shopify")
    elif platform == 'netsuite':
        compare_and_update_prices(products, competitor_prices, update_netsuite_price, platform_name="NetSuite")
    elif platform == 'zoey':
        compare_and_update_prices(products, competitor_prices, update_zoey_price, platform_name="Zoey")

    return {
        'statusCode': 200,
        'body': json.dumps(f"Price comparison and update completed successfully for {platform}!")
    }


# For running locally with Serverless Offline
if __name__ == "__main__":
    event = {
        'platform': 'mock'  # Set to 'mock', 'shopify', 'netsuite', or 'zoey' for testing
    }
    context = {}  # Dummy context for local testing
    lambda_handler(event, context)
