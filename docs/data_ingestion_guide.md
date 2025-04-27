# Data Ingestion Guide

## Input Schema

The data ingestion pipeline supports the following file formats:

### JSON Lines (.json)
Each line should contain a valid JSON object with the following fields:
- `id` (optional): Document identifier. If not provided, an auto-incrementing ID will be assigned.
- `text` (required): The document text content.

Alternative text fields: If `text` is not present, the system will look for `content`, `message`, `body`, or `description`.

Example:
```json
{"id": 1, "text": "This is document 1"}
{"id": 2, "text": "This is document 2"}
{"content": "This document uses the content field"}