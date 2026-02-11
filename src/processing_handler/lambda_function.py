"""
Lambda Processing Handler

- Triggered by S3 ObjectCreated events
- Parses S3 event records and extracts bucket + key
- Writes metadata into DynamoDB for tracking
- Demonstrates event-driven processing and observability via logs
"""

import os
import json
import boto3
from datetime import datetime
import urllib.parse

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    print("✅ S3 EVENT RECEIVED:", json.dumps(event))

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        key = urllib.parse.unquote_plus(key)

        item = {
            "documentId": f"{bucket}/{key}",
            "bucket": bucket,
            "s3Key": key,
            "status": "RECEIVED",
            "timestamp": datetime.utcnow().isoformat()
        }

        print("✅ Writing item:", json.dumps(item))
        table.put_item(Item=item)

    return {"statusCode": 200}
