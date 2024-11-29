"""
Test Databricks functionality with simplified structure
"""
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
FILESTORE_PATH = os.getenv("FILESTORE_PATH", "dbfs:/FileStore/mini_project11")
BASE_URL = f"https://{SERVER_HOSTNAME}/api/2.0"

# Function to check if a DBFS path exists
def check_filestore_path(path):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    try:
        response = requests.get(f"{BASE_URL}/dbfs/get-status?path={path}", headers=headers)
        response.raise_for_status()
        print(f"Path exists: {path}")
        return True  # Path exists if no exception is raised
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to access DBFS path '{path}'. Details: {e}")
        return False

# Test function
def test_databricks():
    print(f"Testing if DBFS path exists: {FILESTORE_PATH}")
    if check_filestore_path(FILESTORE_PATH):
        print(f"Test Passed: DBFS path '{FILESTORE_PATH}' exists.")
    else:
        print(f"Test Failed: DBFS path '{FILESTORE_PATH}' does not exist.")

if __name__ == "__main__":
    test_databricks()


# """
# Test Databricks functionality with simplified structure
# """
# import requests
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# FILESTORE_PATH = "dbfs:/FileStore/mini_project11"
# BASE_URL = f"https://{SERVER_HOSTNAME}/api/2.0"

# # Function to check if a DBFS path exists
# def check_filestore_path(path):
#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
#     try:
#         response = requests.get(f"{BASE_URL}/dbfs/get-status?path={path}", headers=headers)
#         response.raise_for_status()
#         return True  # Path exists if no exception is raised
#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return False

# # Test function
# def test_databricks():
#     assert check_filestore_path(FILESTORE_PATH) is True, f"Path {FILESTORE_PATH} does not exist."

# if __name__ == "__main__":
#     test_databricks()




# from pyspark.sql import SparkSession
# from mylib.extract import extract
# from mylib.transform import transform_data
# from mylib.load import load_data
# from mylib.query import filter_and_save_data

# def create_spark_session():
#     """
#     Initialize a SparkSession.
#     Databricks automatically initializes a SparkSession, so this is simplified.
#     """
#     return SparkSession.builder.getOrCreate()


# def test_extract(spark_session):
#     """
#     Test the extract function.
#     """
#     print("\n=== Starting Extract Test ===")
#     database = "HR_Analytics"
#     raw_table = "Raw_HR_Data"

#     # Execute extract
#     extract(table_name=raw_table, database=database)

#     # Verify table exists in the metastore
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
#     output_dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"

#     # Execute transform
#     transform_data(database, raw_table, transformed_table, output_dbfs_path)

#     # Verify transformed table exists in the metastore
#     if spark.catalog.tableExists(f"{database}.{transformed_table}"):
#         print(f"Transform Test Passed: Table {database}.{transformed_table} exists.")
#     else:
#         print(f"Transform Test Failed: Table {database}.{transformed_table} does not exist.")

#     # Verify DBFS file existence
#     print(f"Checking if transformed data is saved to DBFS at {output_dbfs_path}...")
#     try:
#         files = dbutils.fs.ls(output_dbfs_path)
#         if len(files) > 0:
#             print(f"Transform Test Passed: Files saved in DBFS path {output_dbfs_path}.")
#         else:
#             print(f"Transform Test Failed: No files found in DBFS path {output_dbfs_path}.")
#     except Exception as e:
#         print(f"Transform Test Failed: Unable to access DBFS path {output_dbfs_path} - {e}")

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

#     # Verify filtered table exists in the metastore
#     if spark.catalog.tableExists(f"{database}.{target_table}"):
#         print(f"Query Test Passed: Table {database}.{target_table} exists.")
#     else:
#         print(f"Query Test Failed: Table {database}.{target_table} does not exist.")

#     # Verify the filtered table has expected columns
#     expected_columns = {
#         "EmployeeNumber",
#         "Age",
#         "Attrition",
#         "Department",
#         "Education",
#         "EducationField",
#         "EmployeeCount",
#     }
#     actual_columns = set(field.name for field in spark.table(f"{database}.{target_table}").schema)
#     if expected_columns == actual_columns:
#         print("Query Test Passed: Filtered table columns match expected columns.")
#     else:
#         print(
#             "Query Test Failed: Filtered table columns do not match. "
#             f"Expected: {expected_columns}, Actual: {actual_columns}"
#         )
#     print("=== Query Test Completed ===\n")


# if __name__ == "__main__":
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
#         print("=== Spark Session Stopped ===")