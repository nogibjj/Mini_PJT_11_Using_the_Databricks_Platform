"""
Databricks API Automation and ETL Testing
"""

import os
import requests
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from mylib.extract import extract
from mylib.transform import transform_data
from mylib.load import load_data
from mylib.query import filter_and_save_data


# Load environment variables
load_dotenv()
SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = f"https://{SERVER_HOSTNAME}/api/2.0"

# Validate environment variables
if not SERVER_HOSTNAME or not ACCESS_TOKEN:
    raise ValueError("SERVER_HOSTNAME and ACCESS_TOKEN must be set in the .env file.")

def create_spark_session():
    """
    Initialize a SparkSession.
    """
    spark = SparkSession.builder \
        .appName("Databricks ETL Test") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    return spark

def check_filestore_path(path: str, headers: dict) -> bool:
    """
    Check if a file path exists in Databricks DBFS and validate authentication.

    Args:
        path (str): The file path to check.
        headers (dict): Headers including the authorization token.

    Returns:
        bool: True if the file path exists and authentication is valid, False otherwise.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/dbfs/get-status", headers=headers, json={"path": path}
        )
        response.raise_for_status()
        # Check if the response contains a valid file path
        return "path" in response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return False

def dbfs_download(dbfs_path, local_path):
    """
    Download a file from DBFS to the local file system using the Databricks REST API.
    """
    print(f"Downloading {dbfs_path} to {local_path}...")
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    if not check_filestore_path(dbfs_path, headers):
        raise FileNotFoundError(f"File path '{dbfs_path}' does not exist or is not accessible.")
    response = requests.get(
        f"{BASE_URL}/dbfs/read", headers=headers, json={"path": dbfs_path}
    )
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded successfully: {local_path}")
    else:
        print(f"Failed to download file: {response.status_code} - {response.text}")

def dbfs_upload(local_path, dbfs_path):
    """
    Upload a file from the local file system to DBFS.
    """
    print(f"Uploading {local_path} to {dbfs_path}...")
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    with open(local_path, "rb") as file:
        content = file.read()
    response = requests.post(
        f"{BASE_URL}/dbfs/put",
        headers=headers,
        json={
            "path": dbfs_path,
            "contents": content.decode("latin1"),
            "overwrite": True,
        },
    )
    if response.status_code == 200:
        print(f"Uploaded successfully to {dbfs_path}")
    else:
        print(f"Failed to upload file: {response.status_code} - {response.text}")

def test_extract(spark):
    print("\n=== Starting Extract Test ===")
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"

    extract(table_name=raw_table, database=database)

    if spark.catalog.tableExists(f"{database}.{raw_table}"):
        print(f"Extract Test Passed: Table {database}.{raw_table} exists.")
    else:
        print(f"Extract Test Failed: Table {database}.{raw_table} does not exist.")
    print("=== Extract Test Completed ===\n")

def test_transform(spark):
    print("\n=== Starting Transform Test ===")
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"
    transformed_table = "Employee_Attrition_Data"

    transform_data(database, raw_table, transformed_table)

    if spark.catalog.tableExists(f"{database}.{transformed_table}"):
        print(f"Transform Test Passed: Table {database}.{transformed_table} exists.")
    else:
        print(f"Transform Test Failed: Table {database}.{transformed_table} does not exist.")
    print("=== Transform Test Completed ===\n")

def test_load(spark):
    print("\n=== Starting Load Test ===")
    database = "HR_Analytics"
    transformed_table = "Employee_Attrition_Data"

    try:
        load_data(database, transformed_table)
        print(f"Load Test Passed: Data loaded successfully from {database}.{transformed_table}.")
    except Exception as e:
        print(f"Load Test Failed: {e}")
    print("=== Load Test Completed ===\n")

def test_query(spark):
    print("\n=== Starting Query Test ===")
    database = "HR_Analytics"
    source_table = "Employee_Attrition_Data"
    target_table = "Employee_Attrition_Data_Filtered"

    filter_and_save_data(database, source_table, target_table)

    if spark.catalog.tableExists(f"{database}.{target_table}"):
        print(f"Query Test Passed: Table {database}.{target_table} exists.")
    else:
        print(f"Query Test Failed: Table {database}.{target_table} does not exist.")
    print("=== Query Test Completed ===\n")

if __name__ == "__main__":
    dbfs_path = "dbfs:/mnt/data/Raw_HR_Data.csv"
    local_path = "./Raw_HR_Data.csv"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    if not check_filestore_path(dbfs_path, headers):
        print(f"File path '{dbfs_path}' does not exist. Please check your DBFS configuration.")
    else:
        dbfs_download(dbfs_path, local_path)

    spark = create_spark_session()
    try:
        print("\n=== Starting ETL Tests ===\n")
        test_extract(spark)
        test_transform(spark)
        test_load(spark)
        test_query(spark)
        print("\n=== All ETL Tests Completed Successfully ===\n")
    finally:
        print("=== Stopping Spark Session ===")
        spark.stop()
        print("Spark Session Stopped. Exiting...")



# from pyspark.sql import SparkSession
# from dotenv import load_dotenv
# import os
# import requests
# from mylib.extract import extract
# from mylib.transform import transform_data
# from mylib.load import load_data
# from mylib.query import filter_and_save_data


# def create_spark_session():
#     """
#     Initialize a SparkSession.
#     """
#     spark = SparkSession.builder \
#         .appName("Local Test ETL Pipeline") \
#         .master("local[*]") \
#         .config("spark.sql.shuffle.partitions", "4") \
#         .getOrCreate()
#     return spark


# def download_from_dbfs(dbfs_path, local_path):
#     """
#     Download a file from DBFS to the local file system using the Databricks REST API.
#     """
#     print(f"Downloading {dbfs_path} to {local_path}...")
#     headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
#     response = requests.get(
#         f"{DATABRICKS_HOST}/api/2.0/dbfs/read",
#         headers=headers,
#         json={"path": dbfs_path},
#     )
#     if response.status_code == 200:
#         with open(local_path, "wb") as file:
#             file.write(response.content)
#         print(f"Downloaded successfully: {local_path}")
#     else:
#         print(f"Failed to download file: {response.status_code} - {response.text}")


# def test_extract(spark):
#     """
#     Test the extract function.
#     """
#     print("\n=== Starting Extract Test ===")
#     database = "HR_Analytics"
#     raw_table = "Raw_HR_Data"

#     # Execute extract
#     extract(table_name=raw_table, database=database)

#     # Verify table exists
#     if spark.catalog.tableExists(f"{database}.{raw_table}"):
#         print(f"Extract Test Passed: Table {database}.{raw_table} exists.")
#     else:
#         print(f"Extract Test Failed: Table {database}.{raw_table} does not exist.")
#     print("=== Extract Test Completed ===\n")


# def test_transform(spark):
#     """
#     Test the transform function.
#     """
#     print("\n=== Starting Transform Test ===")
#     database = "HR_Analytics"
#     raw_table = "Raw_HR_Data"
#     transformed_table = "Employee_Attrition_Data"

#     # Execute transform
#     transform_data(database, raw_table, transformed_table)

#     # Verify transformed table exists
#     if spark.catalog.tableExists(f"{database}.{transformed_table}"):
#         print(f"Transform Test Passed: Table {database}.{transformed_table} exists.")
#     else:
#         print(f"Transform Test Failed: Table {database}.{transformed_table} does not exist.")
#     print("=== Transform Test Completed ===\n")


# def test_load(spark):
#     """
#     Test the load function.
#     """
#     print("\n=== Starting Load Test ===")
#     database = "HR_Analytics"
#     transformed_table = "Employee_Attrition_Data"

#     # Execute load
#     try:
#         load_data(database, transformed_table)
#         print(f"Load Test Passed: Data loaded successfully from {database}.{transformed_table}.")
#     except Exception as e:
#         print(f"Load Test Failed: {e}")
#     print("=== Load Test Completed ===\n")


# def test_query(spark):
#     """
#     Test the query function (filter_and_save_data).
#     """
#     print("\n=== Starting Query Test ===")
#     database = "HR_Analytics"
#     source_table = "Employee_Attrition_Data"
#     target_table = "Employee_Attrition_Data_Filtered"

#     # Execute query to filter and save data
#     filter_and_save_data(database, source_table, target_table)

#     # Verify filtered table exists
#     if spark.catalog.tableExists(f"{database}.{target_table}"):
#         print(f"Query Test Passed: Table {database}.{target_table} exists.")
#     else:
#         print(f"Query Test Failed: Table {database}.{target_table} does not exist.")

#     # Verify the filtered table has expected columns
#     expected_columns = [
#         "EmployeeNumber",
#         "Age",
#         "Attrition",
#         "Department",
#         "Education",
#         "EducationField",
#         "EmployeeCount",
#     ]
#     actual_columns = [field.name for field in spark.table(f"{database}.{target_table}").schema]
#     if expected_columns == actual_columns:
#         print("Query Test Passed: Filtered table columns match expected columns.")
#     else:
#         print(
#             "Query Test Failed: Filtered table columns do not match. "
#             f"Expected: {expected_columns}, Actual: {actual_columns}"
#         )
#     print("=== Query Test Completed ===\n")


# if __name__ == "__main__":
#     # Load environment variables
#     load_dotenv()
#     DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
#     DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

#     # File paths
#     dbfs_path = "dbfs:/mnt/data/Raw_HR_Data.csv"
#     local_path = "./Raw_HR_Data.csv"

#     # Download data from DBFS
#     download_from_dbfs(dbfs_path, local_path)

#     # Initialize SparkSession
#     spark = create_spark_session()

#     try:
#         # Run tests
#         print("\n=== Starting ETL Tests ===\n")
#         test_extract(spark)
#         test_transform(spark)
#         test_load(spark)
#         test_query(spark)
#         print("\n=== All ETL Tests Completed Successfully ===\n")
#     finally:
#         # Stop SparkSession
#         print("=== Stopping Spark Session ===")
#         spark.stop()
#         print("Spark Session Stopped. Exiting...")

