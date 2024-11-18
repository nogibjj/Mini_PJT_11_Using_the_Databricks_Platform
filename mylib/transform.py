from pyspark.sql import SparkSession

def transform_data(database, raw_table, transformed_table):
    """
    Transform raw data table into a cleaned version by 
    handling missing values for all columns.

    Args:
        database (str): Databricks database.
        raw_table (str): Name of the raw data table.
        transformed_table (str): Name of the transformed table.

    Returns:
        None
    """
    try:
        # Initialize SparkSession
        spark = SparkSession.builder.getOrCreate()

        # Check if the raw table exists
        if not spark.catalog.tableExists(f"{database}.{raw_table}"):
            print(
                f"Error: Table {database}.{raw_table} does not exist. "
                "Transformation aborted."
            )
            return

        # Load the table schema dynamically
        schema = spark.table(f"{database}.{raw_table}").schema

        # Generate SQL expressions for handling missing values
        column_expressions = []
        for field in schema:
            if str(field.dataType) in [
                'IntegerType', 'DoubleType', 'FloatType', 'LongType'
            ]:  # Numeric columns
                column_expressions.append(
                    f"COALESCE({field.name}, 0) AS {field.name}"
                )
            elif str(field.dataType) == 'StringType':  # String columns
                column_expressions.append(
                    f"COALESCE({field.name}, 'Unknown') AS {field.name}"
                )
            else:  # Other types (default behavior)
                column_expressions.append(field.name)

        # Combine all column expressions
        columns_sql = ",\n".join(column_expressions)

        # Generate SQL query
        query = (
            f"CREATE OR REPLACE TABLE {database}.{transformed_table} AS "
            f"SELECT\n"
            f"{columns_sql}\n"
            f"FROM {database}.{raw_table}"
        )
        
        # Execute the query
        spark.sql(query)
        print(
            f"Transformation successful: Data saved to "
            f"{database}.{transformed_table}"
        )

    except Exception as e:
        print(f"Transformation failed: {e}")
        raise
