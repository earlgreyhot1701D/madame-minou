"""
Madame Minou — Block 0 deploy spike: hello-world Lambda handler.

This validates the AWS Lambda + API Gateway deploy path works.
In production this will be replaced by the /reading and /behavior endpoints.
"""

import json


def lambda_handler(event, context):
    """Minimal hello-world handler for the deploy spike."""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # tighten to CloudFront origin in prod
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps({
            "message": "Bonjour! Madame Minou's crystal ball is warming up...",
            "status": "spike_pass",
            "version": "0.0.1-spike",
        }),
    }
