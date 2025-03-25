# Real-time Stock trading ETL pipeline

## Project Overview
This project is utilzing Spark, Delta Lake, S3 as well as Prefect to create a robust, portable and user-friendly ETL pipeline to discover global stock market trends using Alphavantage API, coupled with data engineering best practices including containerization, workflow orchestration, data lake/lakehosue architecture, spark data prcocessing, deployment automation and more!

This pipeline by default will process near real-time intraday stock trading data into daily aggregate table to provide a holistic view of a given stock time series changes, and it will be deployed using Prefect, an evolutionary workflow scheduling tool which is more competitive than Airflow

## Architecture
### Technology and Tools
  - **Python**: Core programming language used for scripting the ETL processes.
  - **API**: The pipeline uses the Alpha Vantage API to fetch real-time trading data.
  - **PySpark**: Spark is used for distributed data processing and handling large volume dataset
  - **MinIO/S3**: Open-source object storage system used to build data lake solutions and storage raw file
  - **Delta Lake**: Unified governance layer on top of data lake to provide efficient data management and interaction
  - **Docker**: Containerized solution to provide deployment and test automation
  - **Prefect**: Workflow orchestration tool used for trigger ETL process on a given time interval
  - **Makefile**: Used to simplify and manage the execution of tasks within the project, including setup, testing and deployment.

### Architecture Diagram
![image](https://github.com/user-attachments/assets/431b60d9-d23f-451d-b4b0-b928c457c660)

### Deployment Guideline
1. Register free API key: https://www.alphavantage.co/support/#api-key and store it in `godata2023/config/config.ini`
2. and more ...
