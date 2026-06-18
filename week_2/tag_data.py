import os
import sqlite3
import time
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

BATCH_SIZE = 5
RETRY_LIMIT = 3
RETRY_DELAY_SECONDS = 7

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chunk_rows(rows, batch_size):
    for index in range(0, len(rows), batch_size):
        yield rows[index:index + batch_size]

def tag_data(db_url: str):
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source_id, description
        FROM jobs
        WHERE tech_stack IS NULL
    """)

    rows = cursor.fetchall()
    print(f"Found {len(rows)} jobs to tag")

    if not rows:
        conn.close()
        return

    for batch_index, batch in enumerate(chunk_rows(rows, BATCH_SIZE)):
        print(f"\nProcessing Batch {batch_index + 1} with {len(batch)} jobs")

        job_blocks = []

        for source_id, description in batch:
            job_blocks.append(f"""
    Job ID: {source_id}
    Description:
    {description}
    """)

        batch_text = "\n---\n".join(job_blocks)

        prompt = f"""
You will receive multiple job descriptions.

For each Job ID, extract technologies from the description.

Include:
- Programming languages
- Frameworks
- Databases
- Cloud platforms
- Software tools
- Libraries

Exclude:
- Job responsibilities
- Soft skills
- Generic concepts
- Certifications

Return ONLY valid JSON.
Do not include markdown.
Do not include explanation.

Format:
{{
  "JOB_ID": ["skill 1", "skill 2"]
}}

Jobs:
{batch_text}
"""

        result = {}

        for attempt in range(RETRY_LIMIT):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                if not response.text:
                    raise ValueError("Empty response from Gemini")

                result = json.loads(response.text)
                break

            except Exception as error:
                print(f"[Batch {batch_index + 1}] Attempt {attempt + 1} failed: {error}")

                if attempt < RETRY_LIMIT - 1:
                    time.sleep(RETRY_DELAY_SECONDS)
                else:
                    print(f"Skipping Job {source_id}")
                    result = {}

        if not result:
            continue

        for source_id, _description in batch:
            skills = result.get(str(source_id))

            if not skills:
                print(f"Missing result for Job {source_id}")
                tech_stack = "no tech stack extracted"
            else:
                tech_stack = ", ".join(skills)

            cursor.execute("""
                UPDATE jobs
                SET tech_stack = ?
                WHERE source_id = ?
            """, (tech_stack, source_id))

            print(f"Analyzed Job {source_id}: {tech_stack}")

        conn.commit()

        time.sleep(RETRY_DELAY_SECONDS)
    conn.close()

    print("\nDatabase updated!")


if __name__ == "__main__":
    tag_data("data/jobs_d1.db")