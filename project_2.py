from PyPDF2 import PdfReader
from pathlib import Path

BASE = Path("/Users/ashishmokashi/Documents/Python/content")
OUTPUT = BASE / "output1.txt"
FOLDERS = ["One", "Two", "Three"]

def extract_pdf_text(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return "\n\n".join(parts)
    except Exception as e:
        print(f"Failed to read {pdf_path.name}: {e}")
        return ""

def append_pdfs_from_folders():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    for folder in FOLDERS:
        folder_path = BASE / folder
        if not folder_path.exists():
            print(f"Skipping missing folder: {folder_path}")
            continue

        pdf_files = sorted(folder_path.glob("*.pdf")) + sorted(folder_path.glob("*.PDF"))
        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file}")
            text = extract_pdf_text(pdf_file)
            if not text:
                print(f"No text extracted from {pdf_file.name}, skipping.")
                continue
            header = f"\n\n----- START {pdf_file.name} ({folder}) -----\n\n"
            footer = f"\n\n----- END {pdf_file.name} -----\n\n"
            with OUTPUT.open("a", encoding="utf-8") as out:
                out.write(header)
                out.write(text)
                out.write(footer)

if __name__ == "__main__":
    append_pdfs_from_folders()