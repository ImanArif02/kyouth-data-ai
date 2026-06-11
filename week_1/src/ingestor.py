from pathlib import Path
from email import message_from_string
import quopri


def ingest_all_mhtml(input_dir, output_dir):

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    extracted = 0
    failed = 0

    print("🥉 Bronze:")

    for file in input_dir.glob("*.mhtml"):

        total += 1

        try:

            file_content = file.read_text(errors="ignore")

            message = message_from_string(file_content)

            html_content = None

            for part in message.walk():

                if part.get_content_type() == "text/html":

                    payload = part.get_payload()

                    html_content = quopri.decodestring(payload).decode(
                        "utf-8",
                        errors="ignore"
                    )

                    break

            if html_content is None:

                print(f"⚠️ No HTML content found in: {file.name}")
                failed += 1
                continue

            output_file = output_dir / f"{file.stem}.html"

            output_file.write_text(
                html_content,
                encoding="utf-8"
            )

            print(f"✅ Extracted: {file.name}")
            extracted += 1

        except Exception:

            print(f"⚠️ Failed: {file.name}")
            failed += 1

    print("\n📊 Bronze Summary:")
    print(
        f"Total: {total} | Extracted: {extracted} | Failed: {failed}"
    )
    