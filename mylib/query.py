from pyspark.sql import SparkSession

def filter_and_save_data(database, source_table, target_table):
    """
    Filter specific columns from a table and save to a new Delta table.

    Args:
        database (str): Databricks database name.
        source_table (str): Source table to filter data from.
        target_table (str): Target table name to save filtered data.

    Returns:
        None
    """
    spark = SparkSession.builder.getOrCreate()

    # Check if the source table exists
    if not spark.catalog.tableExists(f"{database}.{source_table}"):
        print(f"Error: Table {database}.{source_table} does not exist.")
        return

    # Define the columns to select
    selected_columns = [
        "EmployeeNumber",
        "Age",
        "Attrition",
        "Department",
        "Education",
        "EducationField",
        "EmployeeCount"
    ]

    # Generate SQL query to select only the specified columns
    query = f"""
    CREATE OR REPLACE TABLE {database}.{target_table} AS
    SELECT {', '.join(selected_columns)}
    FROM {database}.{source_table}
    """

    # Execute the query
    try:
        print(f"""Executing query to filter and save data to 
              {database}.{target_table}...""")
        spark.sql(query)
        print(f"""Filtered data saved successfully to 
              {database}.{target_table}.""")
    except Exception as e:
        print(f"""Failed to filter and save data: {e}""")
        raise
