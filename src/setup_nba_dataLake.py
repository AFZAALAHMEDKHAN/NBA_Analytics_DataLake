import boto3
import botocore.exceptions


s3 = boto3.client('s3')
glue = boto3.client('glue')
athena = boto3.client('athena')

bucket_name = "nba-datalake-01"
glue_database_name = "nba_datalake_01"
athena_output_location = f"s3://{bucket_name}/athena-results/"



def create_S3_bucket_if_not_exists():
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
        return
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":  # Bucket not found
            print(f"Bucket '{bucket_name}' not found. Creating it now...")
        else:
            return # this makes sure that all other errors are skipped and does not proceed to create the bucket
            #for cases such as not valid creds etc
    try:
        region = boto3.Session().region_name  # Get default AWS region
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"Bucket '{bucket_name}' created successfully.")

    except Exception as e:
        print(f"Error creating the bucket : {e}")

def create_glue_database_if_not_exists():
    try:
        glue.get_database(Name=glue_database_name)
        print(f"The database {glue_database_name} already exists")
        return 
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            print(f"Database '{glue_database_name}' does not exist. Creating it now...")
        else:
            print(f"Error checking Glue database: {e}")
            return  
    
    try:
        glue.create_database(DatabaseInput={
                "Name" : glue_database_name
            }
        )
        print(f"Successfully created the database {glue_database_name}")
    except Exception as e:
        print(f"Error creating Glue database : {e}")
#we have written the code in a way, handling cases
#of exists and not exists, but for the glue tables, we
#assume that there is no glue table, so we will be creating it.

def create_glue_table():
    try:
        glue.create_table(
            DatabaseName = glue_database_name,
            TableInput = {
                "Name" : "NBA_Players",
                "StorageDescriptor":{
                    'Columns': [
                        {"Name":"PlayerID","Type":"int"},
                        {"Name":"FirstName","Type":"string"},
                        {"Name":"LastName","Type":"string"},
                        {"Name":"Team","Type":"string"},
                        {"Name":"Position","Type":"string"},
                        {"Name":"Points","Type":"int"}
                    ],
                    #since JSON data contains extra fields, Glue will ignore them when querying via Athena.
                    "Location":f"s3://{bucket_name}/raw-data/",
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        print(f"Glue table NBA_Players created successfully")
    except Exception as e:
        print(f"Error creating Glue table :{e}")

def create_glue_table_if_not_exists():
    try:
        tables = glue.get_tables(DatabaseName=glue_database_name)["TableList"]
        for table in tables:
            if table["Name"] == "NBA_Players":
                print("Glue table 'NBA_Players' already exists.")
                return
    except botocore.exceptions.ClientError as e:
        print(f"Error checking Glue tables: {e}")
        return

    create_glue_table()  # Call the existing create_glue_table function


def configure_athena():
    try:
        athena.start_query_execution(
            QueryString="CREATE DATABASE IF NOT EXISTS nba_datalake_01_analytics",
            ResultConfiguration= {"OutputLocation": athena_output_location},
        )
        print("Athena output location configured successfully.")
    
    except Exception as e:
        print(f"Error configuring Athena: {e}")

# Note: This function only creates a database in Athena.
# However, we will not use this Athena database in this project.
# Instead, we will query the Glue database directly in Athena, since AWS Glue Catalog 
# already holds the table schema and references the S3 data.
# If needed, an Athena table can be created to reference the Glue table schema explicitly.


def main():
    create_S3_bucket_if_not_exists()
    create_glue_database_if_not_exists()
    create_glue_table_if_not_exists()
    configure_athena()
    print("Data Lake setup complete")

if __name__ == "__main__":
    main()


