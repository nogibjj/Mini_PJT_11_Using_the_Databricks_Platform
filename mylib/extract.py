"""
Module for extracting data from an external source, cleaning it, and saving to a Delta table.
"""

# Standard library imports
import re

# Third-party library imports
import pandas as pd
from pyspark.sql import SparkSession

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
    hr_dataframe = pd.read_csv(url)
    hr_dataframe.columns = [
        re.sub(r"[^\w]", "_", col.strip()).replace("__", "_")
        for col in hr_dataframe.columns
    ]

    # Convert to Spark DataFrame
    spark_df = spark.createDataFrame(hr_dataframe)

    # Ensure database exists
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

    # Write to Delta table
    spark_df.write.format("delta").mode("overwrite").saveAsTable(
        f"{database}.{table_name}"
    )
    print(f"Data successfully extracted and saved to {database}.{table_name}")
