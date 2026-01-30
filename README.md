# job-market-data-pipeline

Job market Data Engineering Pipeline

This project implements an end-to-end data pipeline that ingests raw job market data, cleans and transforms it, and stores it in a structured, analysis-ready format.
The goal is to simulate how real-world job posting data would be processed in a production-style analytics workflow.

The pipeline is designed with clarity, reproducibility, and scalability in mind, following best practices used in data engineering and analytics roles.



**Project Objectives**

Transform raw, messy job market data into a clean, structured dataset

Design a relational data model suitable for downstream analytics

Apply data cleaning and transformation logic using Python

Store processed data in formats suitable for querying and analysis

Organize the project as a modular, reusable pipeline

**Data Source**

The pipeline operates on publicly available job posting datasets (CSV format), containing information such as:

- Job titles
- Companies
- Locations
- Employment details (e.g. full-time/part-time)
- Descriptions and metadata

The pipeline is intentionally dataset-agnostic and can be adapted to other job market datasets with minimal changes.



**Data Model**

The processed data is structured using a relational model, making it suitable for SQL-based analysis.

Example tables:

jobs — job title, description, company ID, location ID

companies — company name and metadata

locations — city, region, country

This design avoids duplication, improves data integrity, and mirrors real-world analytical databases.




**Key Features & Techniques**

Python-based data processing (pandas, sqlite3)

Data validation and cleaning (missing values, normalization)

Separation of concerns via modular scripts

Reproducible pipeline design

Storage in CSV and SQLite for flexible downstream usage

Clear folder structure aligned with industry conventions



**How to Run the Pipeline**

Clone the repository:

git clone https://github.com/Oswin0905/job-market-data-pipeline.git
cd job-market-data-pipeline


Install dependencies:

pip install -r requirements.txt


Run the pipeline steps:

python src/ingest.py
python src/clean.py
python src/transform.py


Output:

Clean datasets in data/processed/

Structured SQLite database in outputs/
