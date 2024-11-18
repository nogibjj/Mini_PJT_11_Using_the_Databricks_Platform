# Databricks notebook source
dbutils.fs.ls("dbfs:/FileStore/HR_Analytics/Transformed_Data_CSV/")

# COMMAND ----------

# DBFS에서 파일 확인
dbutils.fs.ls("dbfs:/FileStore/HR_Analytics/")
