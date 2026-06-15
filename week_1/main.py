import logging 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

import sys
from pathlib import Path
from src.loader import load_all_jsons
from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html
from src.profiler import run_data_profile

SOURCE_DIR = Path("data/0_source")
BRONZE_DIR = Path("data/1_bronze")
SILVER_DIR = Path("data/2_silver")
GOLD_DIR = Path("data/3_gold")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [ingest|process|load|profile|all]")
        return

    command = sys.argv[1]

    if command == "ingest":
        ingest_all_mhtml(SOURCE_DIR, BRONZE_DIR)
    elif command == "process":
        process_all_html(BRONZE_DIR, SILVER_DIR)
    elif command == "load":
        load_all_jsons(SILVER_DIR, GOLD_DIR)
    elif command == "profile":
        run_data_profile(GOLD_DIR / "jobs.db")
    elif command == "all":
        ingest_all_mhtml( SOURCE_DIR,BRONZE_DIR)

        process_all_html( BRONZE_DIR, SILVER_DIR)

        load_all_jsons(SILVER_DIR, GOLD_DIR)

        run_data_profile(GOLD_DIR / "jobs.db")
    else:
        print("Usage: python main.py [ingest|process|load|profile|all]")

if __name__ == "__main__":
    main()