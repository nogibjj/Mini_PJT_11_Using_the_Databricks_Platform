# main

from mylib.extract import extract
from mylib.transform import transform_data
from mylib.load import load_data
from mylib.query import filter_and_save_data
# import os

# def load_environment():
#     """
#     Load environment variables if running outside of Databricks.
#     """
#     try:
#         # Check if running in Databricks
#         if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
#             from dotenv import load_dotenv
#             load_dotenv()  # Load environment variables from .env file
#             print("Environment variables loaded for local execution.")
#         else:
#             print("Running in Databricks environment. Skipping dotenv.")
#     except Exception as e:
#         print(f"Failed to load environment variables: {e}")
#         raise

def main():
    # """
    # Orchestrates the ETL pipeline, adaptable for both Databricks and local execution.
    # """
    # # Load environment variables for local execution
    # load_environment()

    # # # Set environment-specific variables
    # # server_hostname = os.getenv("SERVER_HOSTNAME")
    # # access_token = os.getenv("ACCESS_TOKEN")

    # # Check if running locally (Databricks skips these checks)
    # if "DATABRICKS_RUNTIME_VERSION" not in os.environ and (not server_hostname or not access_token):
    #     raise ValueError("SERVER_HOSTNAME and ACCESS_TOKEN must be set in the .env file for local execution.")

    # Database and table configuration
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"
    transformed_table = "Employee_Attrition_Data"
    filtered_table = "Employee_Attrition_Data_Filtered"
    dbfs_output_path = "dbfs:/FileStore/HR_Analytics/Transformed_Data_CSV"

    try:
        print("Extracting data...")
        extract(table_name=raw_table, database=database)

        print("Transforming data and saving to DBFS...")
        transform_data(database, raw_table, transformed_table, dbfs_output_path)

        print("Loading data...")
        load_data(database, transformed_table)

        print("Filtering data and saving to new table...")
        filter_and_save_data(database, transformed_table, filtered_table)

        print("ETL pipeline completed successfully.")

    except Exception as e:
        print(f"ETL pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()



# from mylib.extract import extract
# from mylib.transform import transform_data
# from mylib.load import load_data
# from mylib.query import filter_and_save_data

# def main():
#     """
#     Orchestrates the ETL pipeline.
#     """
#     # Database and table configuration
#     database = "HR_Analytics"
#     raw_table = "Raw_HR_Data"
#     transformed_table = "Employee_Attrition_Data"
#     filtered_table = "Employee_Attrition_Data_Filtered"

#     try:
#         print("Extracting data...")
#         extract(table_name=raw_table, database=database)

#         print("Transforming data...")
#         transform_data(database, raw_table, transformed_table)

#         print("Loading data...")
#         load_data(database, transformed_table)

#         print("Filtering data and saving to new table...")
#         filter_and_save_data(database, transformed_table, filtered_table)


#     except Exception as e:
#         print(f"ETL pipeline failed: {e}")
#         raise


# if __name__ == "__main__":
#     main()
