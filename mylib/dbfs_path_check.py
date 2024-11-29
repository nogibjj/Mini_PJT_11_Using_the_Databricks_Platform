files = dbutils.fs.ls("dbfs:/FileStore/mini_project11")
for file in files:
    print(f"File: {file.name}, Size: {file.size}")