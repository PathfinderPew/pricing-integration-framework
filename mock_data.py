# mock_data.py

# Mock product data
mock_products = {
    "products": [
        {"id": 1, "title": "Mock Product 1", "variants": [{"id": 101, "price": "10.00"}]},
        {"id": 2, "title": "Mock Product 2", "variants": [{"id": 102, "price": "15.00"}]}
    ]
}

# Function to get mock products
def get_mock_products():
    return mock_products['products']
