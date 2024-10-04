import boto3
import json

# Set up the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = "PricingProposals"
table = dynamodb.Table(table_name)

def send_to_approval_system(product_id, variant_id, current_price, competitor_price, proposed_price):
    """Sends the proposed price changes to the Approval System (DynamoDB table)."""
    response = table.put_item(
        Item={
            'ProductID': str(product_id),
            'VariantID': str(variant_id),
            'CurrentPrice': current_price,
            'CompetitorPrice': competitor_price,
            'ProposedPrice': proposed_price,
            'ApprovalStatus': 'Pending',  # Initial state
        }
    )
    print(f"Sent proposal for Product {product_id} to approval system.")
    return response
