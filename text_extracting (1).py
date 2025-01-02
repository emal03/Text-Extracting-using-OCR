import os
import boto3
import pandas as pd
import re
import time
from google.colab import files

# AWS Configuration
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_REGION"] = "us-east-1"

# Initialize AWS Clients
s3_client = boto3.client("s3")
textract_client = boto3.client("textract", region_name=os.getenv("AWS_REGION"))

# Function to Upload to S3
def upload_to_s3(file_path, bucket_name, object_name):
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded to S3 bucket {bucket_name} with key {object_name}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# Textract Job Management
def start_textract_job(bucket, key):
    response = textract_client.start_document_analysis(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return response["JobId"]

def check_textract_job_status(job_id):
    while True:
        response = textract_client.get_document_analysis(JobId=job_id)
        if response["JobStatus"] in ["SUCCEEDED", "FAILED"]:
            return response if response["JobStatus"] == "SUCCEEDED" else None
        time.sleep(5)

# Parse Extracted Data
def parse_textract_response(response):
    structured_data = []
    blocks = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']

    # Regex for Field Extraction
    patterns = {
        "Invoice No.": r"Invoice No[:\-]?\s*(\S+)|No[:\-]?\s*(\d+)",
        "TRN No.": r"TRN[:\-]?\s*(\d+)",
        "Date": r"Date[:\-]?\s*(\d{1,2}/\d{1,2}/\d{2,4})",
        "Amount Before VAT": r"(TOTAL BEFORE VAT|Amount Before VAT)[:\-]?\s*(\d+\.\d+)",
        "VAT 5%": r"VAT 5%[:\-]?\s*(\d+\.\d+)",
        "Amount After VAT": r"(TOTAL|Invoice Total)[:\-]?\s*(\d+\.\d+)"
    }

    for i, line in enumerate(blocks):
        extracted = {field: re.search(regex, line) for field, regex in patterns.items()}
        structured_data.append({field: match.group(1) if match else None for field, match in extracted.items()})
    return structured_data

# Save Data to Excel
def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

# Main Workflow
def process_document(file_path, bucket_name, object_name):
    upload_to_s3(file_path, bucket_name, object_name)
    job_id = start_textract_job(bucket_name, object_name)
    response = check_textract_job_status(job_id)
    if response:
        data = parse_textract_response(response)
        save_to_excel(data, "textract_results.xlsx")

# File Upload in Colab
uploaded = files.upload()
file_name = list(uploaded.keys())[0]
bucket_name = ""  # Specify your bucket name
object_name = f"uploads/{file_name}"
process_document(file_name, bucket_name, object_name)
