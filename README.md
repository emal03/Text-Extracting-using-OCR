# Textract Automation Script for Document Processing


This repository offers an autoscale approach to extract tabular data from raw documents using AWS Textract and S3. It will encompass the capability to upload the stored data to an S3 bucket and then utilize Textract to process the data then transfer the extracted information to a database format such as Excel.

Features
AWS Integration: Can easily connect with AWS Textract and S3 for documents’ analysis.
Text and Data Extraction: Digitizes every document containing invoice details such as invoice numbers, invoice dates and VAT amounts.
Excel Export: Saves the extracted data into a locale and exports the locale into an Excel file for ease of analysis and reporting.
Colab Compatibility: Contains the ability for file imports and processing from within the Google’s COLAB environment.
Error Handling: Handling of exception on AWS operations and files.
Workflow

Upload File to S3:
Input documents in a specific S3 bucket through the script.
Textract Analysis:
Use this API to begin a Textract job that interprets uploaded items for structured data.
Data Parsing:
Record several matches of invoice number, TRN number, dates, and accounts, as a mark 1, mark 2, and the like using regex patterns.
Save and Display:
Store extracted data in an excel and print the results in the console or colab.
Usage
Install required Python libraries


