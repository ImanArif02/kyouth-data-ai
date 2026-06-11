from pathlib import Path
import sqlite3

def run_data_profile(db_path):

    db_path = Path(db_path)

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM jobs"

    )

    total_record = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM jobs
    WHERE job_title IS NULL
    OR job_title = ''
    """)

    missing_job_title = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM jobs
    WHERE company IS NULL
    OR company = ''
    """)

    missing_company = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM jobs
    WHERE description IS NULL
    OR description = ''
    """)

    missing_description = cursor.fetchone()[0]

    cursor.execute("""
    SELECT AVG(LENGTH(description))
    FROM jobs
    """)

    avg_description = cursor.fetchone()[0]

    cursor.execute("""
    SELECT source_id,
           job_title,
           LENGTH(description)
    FROM jobs
    ORDER BY LENGTH(description) ASC
    LIMIT 1
    """)

    shortest = cursor.fetchone()

    cursor.execute("""
    SELECT source_id,
           job_title,
           LENGTH(description)
    FROM jobs
    ORDER BY LENGTH(description) DESC
    LIMIT 1
    """)

    longest = cursor.fetchone()

    print("\n--- 🔍 DATA QUALITY REPORT ---")

    print(f"📈 Total Records: {total_record}")

    print(
        f"❓ Missing Values -> "
        f"job_title: {missing_job_title}, "
        f"company: {missing_company}, "
        f"description: {missing_description}"
    )

    print(
        f"📝 Avg Description Length: "
        f"{int(avg_description)} chars"
    )

    print(
        f"⚠️ Shortest Description: "
        f"{shortest[2]} chars"
    )

    print(
        f"   ↳ source_id: {shortest[0]} "
        f"| job_title: {shortest[1]}"
    )

    print(
        f"🚨 Longest Description: "
        f"{longest[2]} chars"
    )

    print(
        f"   ↳ source_id: {longest[0]} "
        f"| job_title: {longest[1]}"
    )

    conn.close()