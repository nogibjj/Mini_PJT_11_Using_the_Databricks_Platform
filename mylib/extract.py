from pyspark.sql import SparkSession
import pandas as pd
import re

def extract(table_name, database="HR_Analytics"):
    """
    Extract data from a predefined URL, clean, and save to Delta table.

    Args:
        table_name (str): Name of the Delta table to create.
        database (str): Databricks database.

    Returns:
        None
    """
    # Define the URL for the dataset
    url = (
        "https://raw.githubusercontent.com/nogibjj/"
        "Mini_PJT_8_Transitioning_from_Python_to_Rust_ISL/main/HR_1.csv"
    )

    # Initialize SparkSession (Databricks environment)
    spark = SparkSession.builder.getOrCreate()

    # Load CSV using pandas
    df = pd.read_csv(url)
    
    # Clean column names: replace invalid characters with underscores
    df.columns = [
        re.sub(r"[^\w]", "_", col.strip()).replace("__", "_") 
        for col in df.columns
    ]

    # Convert pandas DataFrame to Spark DataFrame
    spark_df = spark.createDataFrame(df)

    # Ensure the target database exists
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

    # Write Spark DataFrame to Delta table
    spark_df.write.format("delta") \
        .mode("overwrite") \
        .saveAsTable(f"{database}.{table_name}")
    
    print(f"Data successfully extracted and saved to {database}.{table_name}")


