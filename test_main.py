def check_file_in_dbfs_rest(base_url, access_token, dbfs_path):
    """
    Check if a file exists in DBFS using Databricks REST API.

    Args:
        base_url (str): The base URL for Databricks API.
        access_token (str): The access token for authentication.
        dbfs_path (str): The DBFS path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = f"{base_url}/dbfs/list-status"  # Updated endpoint

    try:
        # REST API request to list files in DBFS
        response = requests.get(endpoint, headers=headers, json={"path": dbfs_path})  # Use GET instead of POST
        if response.status_code == 200:
            files = response.json().get("files", [])
            if files:
                print(f"Files found in DBFS path {dbfs_path}: {[file['path'] for file in files]}")
                return True
            else:
                print(f"No files found in DBFS path {dbfs_path}")
                return False
        else:
            print(f"API Error: {response.json()}")
            return False
    except Exception as e:
        print(f"Error while checking DBFS path {dbfs_path}: {e}")
        return False


# def check_file_in_dbfs_spark(dbfs_path):
#     """
#     Check if a file exists in DBFS using Spark commands.

#     Args:
#         dbfs_path (str): The DBFS path to check.

#     Returns:
#         bool: True if the file exists, False otherwise.
#     """
#     try:
#         files = dbutils.fs.ls(dbfs_path)
#         if files:
#             print(f"Files found in DBFS path {dbfs_path}: {[file.path for file in files]}")
#             return True
#         else:
#             print(f"No files found in DBFS path {dbfs_path}")
#             return False
#     except Exception as e:
#         print(f"Error while checking DBFS path {dbfs_path}: {e}")
#         return False

# # Example usage:
# output_dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"
# if check_file_in_dbfs_spark(output_dbfs_path):
#     print("Files exist in the specified DBFS path.")
# else:
#     print("No files found in the specified DBFS path.")
