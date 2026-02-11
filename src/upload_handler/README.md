# Upload Lambda (API Ingestion)

This Lambda is invoked by API Gateway to accept resume uploads.

## What it does
- Validates allowed file types: PDF, PNG, JPG, JPEG
- Decodes `content_base64` from the request body
- Uploads the file to Amazon S3 under the `uploads/` prefix using a timestamped key

## Environment Variables
- `BUCKET_NAME` — S3 bucket where resumes are stored

## Output
Returns a JSON response with the uploaded `bucket` and `key`.
