import json
from app import lambda_handler

# Define test event simulating a POST request
test_event = {
    "body": json.dumps({
        "prompt": "Tell me about demo day",
        "server": "weavely"  # or "demo"
    })
}

# Simulated AWS Lambda context object (can be empty if unused)
test_context = {}

# Run the Lambda handler
response = lambda_handler(test_event, test_context)

# Pretty-print the response
print("Lambda Response:")
print(json.dumps(response, indent=2))
