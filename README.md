# AWS Serverless Resume Processing System

A secure, cost-efficient, event-driven resume processing pipeline built entirely on managed AWS services.

---

## Overview

This project demonstrates the design and implementation of a production-minded, serverless architecture for securely and efficiently processing resume documents.

The system automatically:

- Accepts resume uploads through a secure API endpoint
- Stores documents in encrypted Amazon S3
- Triggers event-driven processing using AWS Lambda
- Initiates asynchronous document analysis with Amazon Textract
- Stores processing metadata in DynamoDB
- Emits logs and metrics to CloudWatch for observability

The architecture is designed to scale automatically while minimizing operational overhead and idle cost.

---

## Why This Project Matters

This project demonstrates:

- Designing secure, serverless cloud architectures using AWS
- Implementing event-driven workflows with S3 and Lambda
- Applying least-privilege IAM principles
- Integrating managed AI services (Amazon Textract)
- Building observable, cost-efficient production-ready systems
- Investigating and resolving real-world configuration issues in distributed systems

The architecture scales automatically, incurs cost only on usage, and follows cloud-native design best practices.


---

## Architecture

### Logical Architecture

Below is the high-level logical architecture of the system:

![Logical Architecture](./Cloud%20Logical%20Architecture.png)

### Runtime Execution Flow

The following diagram illustrates the runtime execution flow after a resume is uploaded:

![Runtime Flow](./Cloud%20Runtime%20Architecture%20%28execution%20flow%20recap%29.png)

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

## Security Design

- Block Public Access enabled on S3
- Server-side encryption (SSE-S3) enabled by default
- S3 Bucket Key enabled for optimized encryption operations
- Least-privilege IAM roles for each Lambda function
- Separation of upload and processing execution roles
- No broad managed policies (e.g., no `AmazonS3FullAccess`)

Security boundaries are enforced by design, not convention.

---

## Cost Optimization

- Fully serverless (no EC2, no always-on compute)
- DynamoDB on-demand billing
- Lambda pay-per-request compute
- Asynchronous Textract invocation
- Dependency-aware resource cleanup to prevent unnecessary AWS charges

Designed for bursty, small-business workloads.

---

## Technical Highlights

- API Gateway secure HTTPS endpoint for controlled ingestion
- Lambda-based upload validation and storage
- S3 event notifications for automatic downstream triggering
- Asynchronous Textract integration
- DynamoDB metadata tracking (on-demand capacity)
- CloudWatch logging for observability and debugging
- Full resource cleanup to prevent unnecessary AWS charges

---

## Debugging Insight

During integration testing, DynamoDB remained empty despite successful Lambda execution.

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

## AWS Services Used

- **Amazon API Gateway** – Secure HTTPS entry point
- **AWS Lambda** – Upload handler and document processor
- **Amazon S3** – Encrypted object storage and event source
- **Amazon DynamoDB** – Metadata persistence (on-demand billing)
- **Amazon Textract** – Asynchronous AI document analysis
- **Amazon CloudWatch** – Logging and monitoring

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

**Estelle F.**  
Cloud Support Engineer Candidate | AWS Certified (3x) | Cloud & AI Systems  

LinkedIn: https://www.linkedin.com/in/estellets

