import pytest
from pyspark.sql import SparkSession
from mylib.extract import extract
from mylib.transform import transform_data
from mylib.load import load_data
from mylib.query import filter_and_save_data  # query.py 추가


@pytest.fixture(scope="module")
def spark():
    """
    Pytest fixture to initialize a SparkSession for testing.
    """
    spark = SparkSession.builder \
        .appName("Test ETL Pipeline") \
        .getOrCreate()
    yield spark
    spark.stop()


def test_extract(spark):
    """
    Test the extract function.
    """
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"

    # Execute extract
    extract(table_name=raw_table, database=database)

    # Verify table exists
    assert spark.catalog.tableExists(f"{database}.{raw_table}"), (
        f"Table {database}.{raw_table} does not exist after extraction."
    )


def test_transform(spark):
    """
    Test the transform function.
    """
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"
    transformed_table = "Employee_Attrition_Data"

    # Execute transform
    transform_data(database, raw_table, transformed_table)

    # Verify transformed table exists
    assert spark.catalog.tableExists(f"{database}.{transformed_table}"), (
        f"Table {database}.{transformed_table} does not exist after transformation."
    )


def test_load(spark):
    """
    Test the load function.
    """
    database = "HR_Analytics"
    transformed_table = "Employee_Attrition_Data"

    # Execute load
    try:
        load_data(database, transformed_table)
        assert True, (
            f"Load function executed successfully for {database}.{transformed_table}."
        )
    except Exception as e:
        pytest.fail(f"Load function failed: {e}")


def test_query(spark):
    """
    Test the query function (filter_and_save_data).
    """
    database = "HR_Analytics"
    source_table = "Employee_Attrition_Data"
    target_table = "Employee_Attrition_Data_Filtered"

    # Execute query to filter and save data
    filter_and_save_data(database, source_table, target_table)

    # Verify filtered table exists
    assert spark.catalog.tableExists(f"{database}.{target_table}"), (
        f"Table {database}.{target_table} does not exist after filtering and saving."
    )

    # Verify the filtered table has expected columns
    expected_columns = [
        "EmployeeNumber",
        "Age",
        "Attrition",
        "Department",
        "Education",
        "EducationField",
        "EmployeeCount",
    ]
    actual_columns = [
        field.name for field in spark.table(f"{database}.{target_table}").schema
    ]
    assert expected_columns == actual_columns, (
        f"Filtered table columns do not match expected columns. "
        f"Expected: {expected_columns}, Actual: {actual_columns}"
    )
