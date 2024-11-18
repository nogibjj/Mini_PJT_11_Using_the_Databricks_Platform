def check_file_in_dbfs_spark(dbfs_path):
    """
    Check if a file exists in DBFS using Spark commands.

    Args:
        dbfs_path (str): The DBFS path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    try:
        files = dbutils.fs.ls(dbfs_path)
        if files:
            print(f"Files found in DBFS path {dbfs_path}: {[file.path for file in files]}")
            return True
        else:
            print(f"No files found in DBFS path {dbfs_path}")
            return False
    except Exception as e:
        print(f"Error while checking DBFS path {dbfs_path}: {e}")
        return False

# Example usage:
output_dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"
if check_file_in_dbfs_spark(output_dbfs_path):
    print("Files exist in the specified DBFS path.")
else:
    print("No files found in the specified DBFS path.")
