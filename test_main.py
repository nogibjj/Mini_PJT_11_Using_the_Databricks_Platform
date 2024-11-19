import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = f"https://{SERVER_HOSTNAME}/api/2.0"

# Validate environment variables
if not SERVER_HOSTNAME or not ACCESS_TOKEN:
    raise ValueError("SERVER_HOSTNAME and ACCESS_TOKEN must be set in the .env file.")

def check_file_in_dbfs(dbfs_path: str, use_rest: bool = True) -> bool:
    """
    Check if a file exists in DBFS using either REST API or Spark commands.

    Args:
        dbfs_path (str): The DBFS path to check.
        use_rest (bool): Whether to use REST API (True) or Spark commands (False).

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if use_rest:
        # Use Databricks REST API
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        endpoint = f"{BASE_URL}/dbfs/get-status"
        try:
            response = requests.get(endpoint, headers=headers, json={"path": dbfs_path})
            response.raise_for_status()  # Raise error if status code is not 200
            # Check if the file path exists in the response
            if response.status_code == 200 and "path" in response.json():
                print(f"File found in DBFS path {dbfs_path}")
                return True
            elif response.status_code == 404:
                print(f"No file found in DBFS path {dbfs_path}")
                return False
            else:
                print(f"API Error: {response.json()}")
                return False
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except Exception as e:
            print(f"Unexpected error while checking DBFS path {dbfs_path}: {e}")
        return False
    else:
        # Use Spark commands
        try:
            files = dbutils.fs.ls(dbfs_path)
            if files:
                print(f"Files found in DBFS path {dbfs_path}: {[file.path for file in files]}")
                return True
            else:
                print(f"No files found in DBFS path {dbfs_path}")
                return False
        except Exception as e:
            print(f"Error while checking DBFS path {dbfs_path} with Spark: {e}")
            return False

# Example usage:
dbfs_path = "dbfs:/mnt/transformed/Employee_Attrition_Data"

# Check file using REST API
if check_file_in_dbfs(dbfs_path, use_rest=True):
    print("File exists using REST API.")
else:
    print("No file found using REST API.")