import logging
from pathlib import Path
import sqlite3
import json


def load_all_jsons(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    db_path = output_dir / "jobs.db"

    print("🥇 Gold:")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        source_id TEXT PRIMARY KEY,
        job_title TEXT,
        company TEXT,
        description TEXT,
        tech_stack TEXT
    )
    """)

    conn.commit()

    total = 0
    inserted = 0
    skipped = 0

    for file in input_dir.glob("*.json"):
        total += 1

        try:
            json_content = file.read_text(encoding="utf-8")
            job = json.loads(json_content)

            cursor.execute("""
            INSERT OR IGNORE INTO jobs (
                source_id,
                job_title,
                company,
                description,
                tech_stack
            )
            VALUES (?, ?, ?, ?, ?)
            """, (
                job["source_id"],
                job["job_title"],
                job["company"],
                job["description"],
                ""
            ))

            if cursor.rowcount == 1:
                inserted += 1
                logging.info(f"Inserted: {file.name}")
            else:
                skipped += 1
                logging.warning(f"Skipped duplicate: {file.name}")

        except Exception as e:
            skipped += 1
            logging.error(f"Failed: {file.name} - {e}")

    conn.commit()
    conn.close()

    print("\n📊 Gold Summary:")
    print(f"Total: {total} | Inserted: {inserted} | Skipped: {skipped}")