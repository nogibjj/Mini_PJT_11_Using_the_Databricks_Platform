from pyspark.sql import SparkSession
import pandas as pd
import re

def extract(table_name, database="HR_Analytics"):
    """
    Extract data from a predefined URL, clean, and save to Delta table.

    Args:ㅌ
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


# extract

# import os
# import re
# import pandas as pd
# from pyspark.sql import SparkSession

# # Retrieve environment variables
# server_h = os.getenv("SERVER_HOSTNAME")
# access_token = os.getenv("ACCESS_TOKEN")
# FILESTORE_PATH = os.getenv("FILESTORE_PATH", "dbfs:/FileStore/mini_project11")
# headers = {'Authorization': f'Bearer {access_token}'}
# api_url = f"https://{server_h}/api/2.0"

# def extract(table_name, database="HR_Analytics", output_path=FILESTORE_PATH):
#     """
#     Extract data from a predefined URL, clean, and save to Delta table and DBFS as a CSV file.

#     Args:
#         table_name (str): Name of the Delta table to create.
#         database (str): Databricks database.
#         output_path (str): DBFS path to save the transformed data as CSV.

#     Returns:
#         str: Full path of the saved CSV file.
#     """
#     try:
#         # Define the URL for the dataset
#         url = (
#             "https://raw.githubusercontent.com/nogibjj/"
#             "Mini_PJT_8_Transitioning_from_Python_to_Rust_ISL/main/HR_1.csv"
#         )
#         print(f"Starting extraction process for table: {table_name}...")

#         # Initialize SparkSession (Databricks environment)
#         spark = SparkSession.builder.getOrCreate()
#         print("SparkSession initialized.")

#         # Load CSV using pandas
#         print(f"Downloading dataset from {url}...")
#         df = pd.read_csv(url)
#         print("Dataset downloaded successfully.")

#         # Clean column names: replace invalid characters with underscores
#         df.columns = [
#             re.sub(r"[^\w]", "_", col.strip()).replace("__", "_") 
#             for col in df.columns
#         ]
#         print("Column names cleaned.")

#         # Convert pandas DataFrame to Spark DataFrame
#         spark_df = spark.createDataFrame(df)
#         print("Pandas DataFrame converted to Spark DataFrame.")

#         # Ensure the target database exists
#         spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")
#         print(f"Database {database} ensured to exist.")

#         # Write Spark DataFrame to Delta table
#         spark_df.write.format("delta") \
#             .mode("overwrite") \
#             .saveAsTable(f"{database}.{table_name}")
#         print(f"Data successfully saved to Delta table: {database}.{table_name}")

#         # Define the full path for the CSV file in DBFS
#         output_file = f"{output_path}/{table_name}_cleaned.csv"

#         # Save the transformed data to DBFS in CSV format
#         print(f"Saving transformed data to DBFS at {output_file}...")
#         spark_df.write.csv(output_file, mode="overwrite", header=True)
#         print(f"Transformed data successfully saved to DBFS as CSV: {output_file}")

#         # Final success message
#         print(f"Extraction process completed successfully for table: {table_name}.")
#         return output_file

#     except Exception as e:
#         print(f"Extraction failed: {e}")
#         raise

# # Example usage
# if __name__ == "__main__":
#     try:
#         table_name = "raw_hr_data"
#         output_file = extract(table_name)
#         print(f"Extraction completed. File saved at: {output_file}")
#     except Exception as e:
#         print(f"An error occurred during the extraction process: {e}")


# Backup