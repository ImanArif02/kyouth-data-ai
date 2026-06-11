# kyouth-data-ai
42 Malaysia K-Youth 2026 Programme – Python for Real-World Data & AI

# K-Youth Data AI - Week 1

## Project Description

This project is part of the 42 Malaysia K-Youth 2026 Programme – Python for Real-World Data & AI.

The objective of this project is to build a simple ETL pipeline that extracts job posting data from JobStreet MHTML files, transforms the data into a structured format, and loads it into a SQLite database for analysis.

The project follows the Medallion Architecture approach:

* 0_source → Raw MHTML files
* 1_bronze → Extracted HTML files
* 2_silver → Cleaned JSON files
* 3_gold → SQLite database

---

## Setup Instructions

### Prerequisites

* Python 3.10 or above
* Git

### Install Dependencies

```bash
pip install beautifulsoup4 pydantic
```

### Clone Repository

```bash
git clone <your-repository-url>
cd kyouth-data-ai/week_1
```

---

## How To Run The Project

### Step 1 - Extract MHTML Files

```bash
python main.py ingest
```

This command extracts raw MHTML files from the source folder and saves them as HTML files in the bronze layer.

---

### Step 2 - Process HTML Files

```bash
python main.py process
```

This command extracts the following fields:

* source_id
* job_title
* company
* description

The cleaned data will be saved as JSON files in the silver layer.

---

### Step 3 - Load Into Database

```bash
python main.py load
```

This command loads all JSON files into a SQLite database located in the gold layer.

---

### Step 4 - Run Data Profiling

```bash
python main.py profile
```

This command generates a simple data quality report, including:

* Total records
* Missing values
* Average description length
* Shortest description
* Longest description

---

### Run Everything At Once

```bash
python main.py all
```

This command executes the entire ETL pipeline from start to finish.

---

## Project Structure

```text
week_1/
│
├── data/
│   ├── 0_source/
│   ├── 1_bronze/
│   ├── 2_silver/
│   └── 3_gold/
│
├── src/
│   ├── ingestor.py
│   ├── processor.py
│   ├── loader.py
│   └── profiler.py
│
├── main.py
└── README.md
```

---

# Technical Reflections

## Day 1 - The Extractor

Keeping the original raw HTML files is useful because we can always refer back to the source data whenever there is an issue during processing. It also allows us to rerun the pipeline without needing to collect the data again.

---

## Day 2 - Treatment Plant

Loading raw data before transforming it provides more flexibility because we can change the transformation logic later if requirements change. Processing files one by one may become slow when the dataset grows larger, while distributed processing can improve performance by handling multiple files at the same time.

---

## Day 3 - The Blueprint & The Vault

Important fields such as job_title should be validated before loading data into the database. If critical information is missing, the record should be rejected to maintain data quality. Using INSERT OR IGNORE also helps prevent duplicate records from being inserted.

---

## Day 4 - The QA Inspector & Orchestrator

If the processing stage fails halfway through, some records may be processed while others remain incomplete. In real-world environments, orchestration tools such as Apache Airflow can automatically manage retries, scheduling, and monitoring to improve reliability.
