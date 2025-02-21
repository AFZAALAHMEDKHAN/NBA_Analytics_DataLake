# 🏀 NBA Data Lake & Analytics Pipeline  

## 📌 Project Overview  
This project builds a **serverless data lake** using AWS services to **ingest, store, and analyze** NBA player data efficiently. The data is fetched from an external sports API, stored in **Amazon S3**, and queried using **Amazon Athena** via **AWS Glue Catalog**.  

## 🚀 Tech Stack  
- **AWS S3** – Storage for raw & processed data  
- **AWS Glue** – Schema management & data catalog  
- **Amazon Athena** – Serverless SQL querying  
- **AWS Lambda (Upcoming)** – Automating data pipeline  
- **Amazon EventBridge (Upcoming)** – Scheduling updates  
- **Python (Boto3, Requests)** – Automating AWS operations & data fetching  

## 🏗️ Project Workflow  
1. **Data Ingestion**: Fetch **real-time NBA player stats** from an API using Python.  
2. **Storage**: Store JSONL-formatted data in **Amazon S3** for efficient querying.  
3. **Schema Management**: Define the table schema in **AWS Glue Catalog**.  
4. **Querying**: Use **Amazon Athena** to run SQL queries on the dataset.  
5. **Future Enhancements**: Automate data updates with **Lambda & EventBridge**.


