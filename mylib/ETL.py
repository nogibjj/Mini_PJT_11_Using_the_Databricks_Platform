import requests
from dotenv import load_dotenv
import os
import json
import base64

# Load environment variables
load_dotenv()
server_h = os.getenv("SERVER_HOSTNAME")
access_token = os.getenv("ACCESS_TOKEN")
FILESTORE_PATH = "dbfs:/FileStore/Mini_PJT_11_Using_the_Databricks_Platform"
headers = {"Authorization": "Bearer %s" % access_token}
url = "https://" + server_h + "/api/2.0"


def perform_query(path, headers, data={}):
    session = requests.Session()
    resp = session.request(
        "POST", url + path, data=json.dumps(data), verify=True, headers=headers
    )
    try:
        return resp.json()
    except ValueError:
        print(f"Invalid JSON response: {resp.text}")
        raise


# List the files in a directory
def mkdirs(path, headers):
    _data = {}
    _data["path"] = path
    return perform_query("/dbfs/mkdirs", headers=headers, data=_data)


# Create a file
def create(path, overwrite, headers):
    _data = {"path": path, "overwrite": overwrite}
    response = perform_query("/dbfs/create", headers=headers, data=_data)
    print("Create Response:", response)  # 디버깅을 위해 출력
    if "handle" not in response:
        raise ValueError(f"Error creating file at {path}. Response: {response}")
    return response


# Add a block to a file
def add_block(handle, data, headers):
    _data = {}
    _data["handle"] = handle
    _data["data"] = data
    return perform_query("/dbfs/add-block", headers=headers, data=_data)


# Close the file
def close(handle, headers):
    _data = {}
    _data["handle"] = handle
    return perform_query("/dbfs/close", headers=headers, data=_data)


# Down load file from url and upload to dbfs
def put_file_from_url(url, dbfs_path, overwrite, headers):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        handle = create(dbfs_path, overwrite, headers=headers)["handle"]
        print("Putting file: " + dbfs_path)
        for i in range(0, len(content), 2**20):
            add_block(
                handle,
                base64.standard_b64encode(content[i : i + 2**20]).decode(),
                headers=headers,
            )
        close(handle, headers=headers)
        print(f"File {dbfs_path} uploaded successfully.")
    else:
        print(f"Error downloading file from {url}. Status code: {response.status_code}")


# Extract data from a URL
def extract(
    url="""https://raw.githubusercontent.com/nogibjj/Mini_PJT_8_Transitioning_from_Python_to_Rust_ISL/refs/heads/main/HR_1.csv""",
    file_path=FILESTORE_PATH + "/HR_1.csv",
    directory=FILESTORE_PATH,
    overwrite=True,
):
    mkdirs(path=directory, headers=headers)
    put_file_from_url(url, file_path, overwrite, headers=headers)

    return file_path


if __name__ == "__main__":
    extract()

    # ## extra

    # df = pd.read_csv(url)
    # print(df.head())
    # event_time_df = spark.createDataFrame(df)
    # event_times_df.write.format()
