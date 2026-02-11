# AWS Serverless Resume Processing System

Secure, cost-efficient, event-driven document processing pipeline built on AWS using managed, pay-per-use services.

---

## Overview

This project demonstrates how to design and implement a production-minded, serverless architecture for processing resumes securely and efficiently.

The system automatically:

- Accepts resume uploads through a secure API endpoint
- Stores documents in encrypted Amazon S3
- Triggers event-driven processing using AWS Lambda
- Initiates asynchronous document analysis with Amazon Textract
- Stores processing metadata in DynamoDB
- Emits logs and metrics to CloudWatch for observability

The architecture is designed to scale automatically while minimizing operational overhead and idle cost.

---

## Architecture

### Logical Architecture

![Logical Architecture](./Cloud%20Logical%20Architecture.png)

### Runtime Execution Flow

![Runtime Flow](./Cloud%20Runtime%20Architecture%20%28execution%20flow%20recap%29.png)

---

## AWS Services Used

- **Amazon API Gateway** – Secure HTTPS entry point
- **AWS Lambda** – Upload handler and document processor
- **Amazon S3** – Encrypted object storage and event source
- **Amazon DynamoDB** – Metadata persistence (on-demand billing)
- **Amazon Textract** – Asynchronous AI document analysis
- **Amazon CloudWatch** – Logging and monitoring

---

## Security Design

- Block Public Access enabled on S3
- Server-side encryption (SSE-S3) enabled by default
- S3 Bucket Key enabled for optimized encryption operations
- Least-privilege IAM roles for each Lambda function
- Separation of upload and processing execution roles
- No broad managed policies (e.g., no `AmazonS3FullAccess`)

Security boundaries are enforced by design, not convention.

---

## Event-Driven Architecture

The system uses S3 ObjectCreated events to trigger downstream processing automatically.

Flow:

1. Resume uploaded via API Gateway
2. Upload Lambda validates and stores file in S3 (`uploads/` prefix)
3. S3 emits ObjectCreated event
4. Processing Lambda starts asynchronous Textract job
5. Job metadata persisted in DynamoDB
6. Logs emitted to CloudWatch

No polling. No idle infrastructure. Fully reactive.

---

## Cost Optimization

- Fully serverless (no EC2, no always-on compute)
- DynamoDB on-demand billing
- Lambda pay-per-request compute
- Asynchronous Textract invocation
- Full resource cleanup after validation

Designed for bursty, small-business workloads.

---

## Debugging Insight

During testing, DynamoDB remained empty even though the processing Lambda executed.

### Investigation Steps

- Verified Lambda execution in CloudWatch logs
- Confirmed IAM permissions were correct
- Checked DynamoDB write logic
- Reviewed S3 event notification configuration
- Inspected object keys in S3

### Root Cause

S3 object keys are case-sensitive.

The event notification prefix was configured as:

uploads/

But files were uploaded under:

Uploads/


### Fix

Aligned prefix casing between S3 folder and event notification.

### Result

S3 events triggered correctly and DynamoDB records appeared immediately.

---

## Key Engineering Principles Demonstrated

- Serverless architecture
- Event-driven design
- Least privilege IAM
- Secure-by-default storage
- Cost-aware cloud engineering
- Production-grade observability

---

## Future Improvements

- Infrastructure as Code (AWS CDK / CloudFormation)
- CI/CD pipeline integration
- Textract result consumption workflow
- Authentication and authorization layer

---

## Author

Estelle F.  
Cloud Engineering Student | AWS Certified | Building in Public 🚀


