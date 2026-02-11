"""
Lambda Upload Handler

- Validates file type
- Decodes base64 file input
- Stores object securely in S3 under uploads/ prefix
- Designed for serverless, event-driven architectures
"""


import json
import os
import base64
import boto3
from datetime import datetime

s3 = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

def _is_allowed_filename(filename: str) -> bool:
    filename = filename.lower().strip()
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def lambda_handler(event, context):
    """
    Expected event body (JSON):
    {
      "filename": "resume.pdf",
      "content_base64": "<base64-encoded file bytes>"
    }
    """

    try:
        body = event.get("body", event)
        if isinstance(body, str):
            body = json.loads(body)

        filename = body.get("filename")
        content_base64 = body.get("content_base64")

        if not filename or not content_base64:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "filename and content_base64 are required"})
            }

        if not _is_allowed_filename(filename):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid file type. Allowed: pdf, png, jpg, jpeg"})
            }

        # Decode file bytes
        file_bytes = base64.b64decode(content_base64)

        # Store in uploads/ prefix with timestamp for uniqueness
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        s3_key = f"uploads/{timestamp}-{filename}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Upload successful",
                "bucket": BUCKET_NAME,
                "key": s3_key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Upload failed", "error": str(e)})
        }
