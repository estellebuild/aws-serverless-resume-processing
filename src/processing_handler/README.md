# Processing Lambda (Event Handler)

This Lambda is triggered by S3 `ObjectCreated` events when a resume lands in the `uploads/` prefix.

## What it does
- Receives S3 event notifications
- Extracts `bucket` and `key` (URL-decodes key)
- Writes a tracking record into DynamoDB with status `RECEIVED`
- Logs the received event + written item to CloudWatch

## Environment Variables
- `TABLE_NAME` — DynamoDB table name for metadata tracking

## Note on common pitfall (case-sensitive prefix)
S3 object keys are case-sensitive. If your event notification uses `uploads/` but objects are stored under `Uploads/`, the trigger will not fire.
