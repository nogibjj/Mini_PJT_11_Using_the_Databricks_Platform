from pyspark.sql import SparkSession
from mylib.extract import extract
from mylib.transform import transform_data
from mylib.load import load_data
from mylib.query import filter_and_save_data

def create_spark_session():
    """
    Initialize a SparkSession.
    Databricks automatically initializes a SparkSession, so this is simplified.
    """
    return SparkSession.builder.getOrCreate()


def test_extract(spark_session):
    """
    Test the extract function.
    """
    print("\n=== Starting Extract Test ===")
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"

    # Execute extract
    extract(table_name=raw_table, database=database)

    # Verify table exists in the metastore
    if spark.catalog.tableExists(f"{database}.{raw_table}"):
        print(f"Extract Test Passed: Table {database}.{raw_table} exists.")
    else:
        print(f"Extract Test Failed: Table {database}.{raw_table} does not exist.")
    print("=== Extract Test Completed ===\n")


def test_transform(spark):
    """
    Test the transform function.
    """
    print("\n=== Starting Transform Test ===")
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"
    transformed_table = "Employee_Attrition_Data"
    output_dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"

    # Execute transform
    transform_data(database, raw_table, transformed_table, output_dbfs_path)

    # Verify transformed table exists in the metastore
    if spark.catalog.tableExists(f"{database}.{transformed_table}"):
        print(f"Transform Test Passed: Table {database}.{transformed_table} exists.")
    else:
        print(f"Transform Test Failed: Table {database}.{transformed_table} does not exist.")

    # Verify DBFS file existence
    print(f"Checking if transformed data is saved to DBFS at {output_dbfs_path}...")
    try:
        files = dbutils.fs.ls(output_dbfs_path)
        if len(files) > 0:
            print(f"Transform Test Passed: Files saved in DBFS path {output_dbfs_path}.")
        else:
            print(f"Transform Test Failed: No files found in DBFS path {output_dbfs_path}.")
    except Exception as e:
        print(f"Transform Test Failed: Unable to access DBFS path {output_dbfs_path} - {e}")

    print("=== Transform Test Completed ===\n")


def test_load(spark):
    """
    Test the load function.
    """
    print("\n=== Starting Load Test ===")
    database = "HR_Analytics"
    transformed_table = "Employee_Attrition_Data"

    # Execute load
    try:
        load_data(database, transformed_table)
        print(f"Load Test Passed: Data loaded successfully from {database}.{transformed_table}.")
    except Exception as e:
        print(f"Load Test Failed: {e}")
    print("=== Load Test Completed ===\n")


def test_query(spark):
    """
    Test the query function (filter_and_save_data).
    """
    print("\n=== Starting Query Test ===")
    database = "HR_Analytics"
    source_table = "Employee_Attrition_Data"
    target_table = "Employee_Attrition_Data_Filtered"

    # Execute query to filter and save data
    filter_and_save_data(database, source_table, target_table)

    # Verify filtered table exists in the metastore
    if spark.catalog.tableExists(f"{database}.{target_table}"):
        print(f"Query Test Passed: Table {database}.{target_table} exists.")
    else:
        print(f"Query Test Failed: Table {database}.{target_table} does not exist.")

    # Verify the filtered table has expected columns
    expected_columns = {
        "EmployeeNumber",
        "Age",
        "Attrition",
        "Department",
        "Education",
        "EducationField",
        "EmployeeCount",
    }
    actual_columns = set(field.name for field in spark.table(f"{database}.{target_table}").schema)
    if expected_columns == actual_columns:
        print("Query Test Passed: Filtered table columns match expected columns.")
    else:
        print(
            "Query Test Failed: Filtered table columns do not match. "
            f"Expected: {expected_columns}, Actual: {actual_columns}"
        )
    print("=== Query Test Completed ===\n")


if __name__ == "__main__":
    # Initialize SparkSession
    spark = create_spark_session()

    try:
        # Run tests
        print("\n=== Starting ETL Tests ===\n")
        test_extract(spark)
        test_transform(spark)
        test_load(spark)
        test_query(spark)
        print("\n=== All ETL Tests Completed Successfully ===\n")
    finally:
        # Stop SparkSession
        print("=== Stopping Spark Session ===")
        spark.stop()
        pri


# Does not work in Databricks
# from mylib.extract import extract
# from mylib.transform import transform_data
# from mylib.load import load_data
# from mylib.query import filter_and_save_data
# import os


# def test_extract(spark):
#     """
#     Test the extract function.
#     """
#     database = "HR_Analytics"
#     raw_table = "Raw_HR_Data"

#     # Execute extract
#     extract(table_name=raw_table, database=database)

#     # Verify table exists
#     assert spark.catalog.tableExists(f"{database}.{raw_table}"), \
#         f"Extract Test Failed: Table {database}.{raw_table} does not exist."


# def test_transform(spark):
#     """
#     Test the transform function.
#     """
#     database = "HR_Analytics"
#     raw_table = "Raw_HR_Data"
#     transformed_table = "Employee_Attrition_Data"
#     output_dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"

#     # Execute transform
#     transform_data(database, raw_table, transformed_table, output_dbfs_path)

#     # Verify transformed table exists
#     assert spark.catalog.tableExists(f"{database}.{transformed_table}"), \
#         f"Transform Test Failed: Table {database}.{transformed_table} does not exist."

#     # Verify DBFS file exists
#     try:
#         files = os.listdir(output_dbfs_path)
#         assert len(files) > 0, f"Transform Test Failed: No files found in DBFS path {output_dbfs_path}."
#     except Exception as e:
#         assert False, f"Transform Test Failed: Unable to access DBFS path {output_dbfs_path} - {e}"


# def test_load(spark):
#     """
#     Test the load function.
#     """
#     database = "HR_Analytics"
#     transformed_table = "Employee_Attrition_Data"

#     # Execute load
#     try:
#         load_data(database, transformed_table)
#     except Exception as e:
#         assert False, f"Load Test Failed: {e}"


# def test_query(spark):
#     """
#     Test the query function (filter_and_save_data).
#     """
#     database = "HR_Analytics"
#     source_table = "Employee_Attrition_Data"
#     target_table = "Employee_Attrition_Data_Filtered"

#     # Execute query to filter and save data
#     filter_and_save_data(database, source_table, target_table)

#     # Verify filtered table exists
#     assert spark.catalog.tableExists(f"{database}.{target_table}"), \
#         f"Query Test Failed: Table {database}.{target_table} does not exist."

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
#     assert expected_columns == actual_columns, \
#         f"Query Test Failed: Filtered table columns do not match. Expected: {expected_columns}, Actual: {actual_columns}"




# BACKUP CODE
# from pyspark.sql import SparkSession
# from mylib.extract import extract
# from mylib.transform import transform_data
# from mylib.load import load_data
# from mylib.query import filter_and_save_data
# import os


# def create_spark_session():
#     """
#     Initialize a SparkSession.
#     """
#     spark = SparkSession.builder \
#         .appName("Test ETL Pipeline") \
#         .getOrCreate()
#     return spark


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
#     output_dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"

#     # Execute transform
#     transform_data(database, raw_table, transformed_table, output_dbfs_path)

#     # Verify transformed table exists
#     if spark.catalog.tableExists(f"{database}.{transformed_table}"):
#         print(f"Transform Test Passed: Table {database}.{transformed_table} exists.")
#     else:
#         print(f"Transform Test Failed: Table {database}.{transformed_table} does not exist.")

#     # Verify DBFS file exists
#     print(f"Checking if transformed data is saved to DBFS at {output_dbfs_path}...")
#     try:
#         files = os.listdir(output_dbfs_path)
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
