from mylib.extract import extract
from mylib.transform import transform_data
from mylib.load import load_data
from mylib.query import filter_and_save_data

def main():
    """
    Orchestrates the ETL pipeline.
    """
    # Database and table configuration
    database = "HR_Analytics"
    raw_table = "Raw_HR_Data"
    transformed_table = "Employee_Attrition_Data"
    filtered_table = "Employee_Attrition_Data_Filtered"

    try:
        print("Extracting data...")
        extract(table_name=raw_table, database=database)

        print("Transforming data...")
        transform_data(database, raw_table, transformed_table)

        print("Loading data...")
        load_data(database, transformed_table)

        print("Filtering data and saving to new table...")
        filter_and_save_data(database, transformed_table, filtered_table)


    except Exception as e:
        print(f"ETL pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()

