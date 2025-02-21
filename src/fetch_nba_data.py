import os
import json
from dotenv import load_dotenv
import requests
import boto3
load_dotenv()

s3 = boto3.client('s3')
bucket_name = "nba-datalake-01"
api_key = os.getenv("SPORTS_DATA_API_KEY")
nba_endpoint = os.getenv("NBA_ENDPOINT")


def fetch_NBA_data():
    headers = {"Ocp-Apim-Subscription-Key":api_key}
#can also use  query parameter, as The API key can be passed either as a query parameter or using the following HTTP request header.
#Ocp-Apim-Subscription-Key: {key}
    try:
        response = requests.get(nba_endpoint,headers=headers)
        response.raise_for_status()
        print("Fetched NBA Data Successfully")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data : {e}")
        return []
    


def convert_to_line_delimited_json(data):
    return "\n".join([json.dumps(record) for record in data])

def save_processed_data_to_S3(data):
    try:
        converted_data = convert_to_line_delimited_json(data)
        file_key = "raw-data/nba_player_data.jsonl"
        s3.put_object(
            Bucket=bucket_name,
            Key = file_key,
            Body = converted_data
        )
        print(f"Successfully saved data to S3 : {file_key}")
        return True
    except Exception as e:
        print(f"error uploading the data to S3: {e}")
        return False
    
def main():
    data = fetch_NBA_data()
    if data:
        save_processed_data_to_S3(data)


if __name__ == "__main__":
    main()