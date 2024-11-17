from pyspark.sql import SparkSession


def load_data(database, table_name):
    """
    Load transformed data into its final destination.

    Args:
        database (str): Databricks database.
        table_name (str): Name of the table to load.

    Returns:
        None
    """
    spark = SparkSession.builder.getOrCreate()

    # Check if the table exists
    if not spark.catalog.tableExists(f"{database}.{table_name}"):
        print(
            f"Error: Table {database}.{table_name} does not exist. "
            "Please verify the table name and database."
        )
        return

    # Display the data from the table
    query = f"SELECT * FROM `{database}`.`{table_name}`"
    print(f"Executing query: {query}")
    spark.sql(query).show()
    print(f"Data from {database}.{table_name} loaded successfully.")


if __name__ == "__main__":
    # Define database and table names
    database_name = "HR_Analytics"  # Example: your Databricks database name
    table_name = "Employee_Attrition_Data"  # Example: your table name

    # Execute the load function
    load_data(database_name, table_name)
