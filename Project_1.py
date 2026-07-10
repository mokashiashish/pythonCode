with open('/Users/ashishmokashi/Documents/Python/content/My_Proj_1_txt.txt',mode= 'r') as projet_1_txt:
   my_new_file = projet_1_txt.read()
   print (my_new_file)
   projet_1_txt.close()

#Project 1: Extract text from PDF file and write to a text file
import json
import re
from PyPDF2 import PdfReader
from pathlib import Path
from sqlite3 import Connection

from db import init_db, ensure_table, insert_question, close_db

pdf_path = Path("/Users/ashishmokashi/Documents/Python/content/Chemistry Questions.pdf")
#txt_path = pdf_path.with_suffix(".txt"
txt_path = Path("/Users/ashishmokashi/Documents/Python/content/output.txt")

reader = PdfReader(str(pdf_path))
all_text = []
for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        all_text.append(page_text)

with open(txt_path, "w", encoding="utf-8") as out:
    out.write("\n\n".join(all_text))

print(f"Wrote extracted PDF file text to: {txt_path}")

with open("/Users/ashishmokashi/Documents/Python/content/output.txt", "a") as in_file:
    in_file.write("\n\nThis is some additional text appended to the file.") 
    in_file.close()


#Project 3 read the specific page from the file and output the content to new file************
import sys

BASE = Path("/Users/ashishmokashi/Documents/Python/content")
CONFIG_FILENAME = "config.json"


def load_config() -> dict:
    cfg_path = BASE / CONFIG_FILENAME
    if not cfg_path.exists():
        print(f"No configuration file found at: {cfg_path}. Proceeding without regex.")
        return {}
    try:
        with cfg_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:
        print(f"Failed to load config {cfg_path}: {e}")
        print("Proceeding without regex configuration.")
        return {}


def extract_matches(text: str, pattern: str) -> list:
    if not text:
        return []
    try:
        matches = re.findall(pattern, text, flags=re.DOTALL)
    except re.error as e:
        print(f"Invalid regex pattern: {e}")
        print("Please check the 'regex' value in the configuration file.")
        return []

    processed = []
    for m in matches:
        if isinstance(m, tuple):
            processed.append("".join(m))
        else:
            processed.append(m)

    return processed

def ensure_content_folder():
    if not BASE.exists():
        print(f"Content folder not found: {BASE}")
        try:
            BASE.mkdir(parents=True, exist_ok=True)
            print(f"Created missing content folder: {BASE}")
        except Exception as e:
            print(f"Failed to create content folder: {e}")
            print("Please create the folder manually or adjust the BASE path and re-run.")
            sys.exit(1)

def find_pdfs():
    pdfs = sorted(BASE.rglob("*.pdf")) + sorted(BASE.rglob("*.PDF"))
    return list(dict.fromkeys(pdfs))  # remove duplicates if any

def choose_pdf(pdfs):
    if not pdfs:
        print("No PDF files found under the content folder or its subfolders.")
        return None
    if len(pdfs) == 1:
        return pdfs[0]
    print("Found multiple PDF files:")
    for i, p in enumerate(pdfs, start=1):
        print(f"{i}: {p}")
    while True:
        choice = input(f"Select a file by number (1-{len(pdfs)}): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(pdfs):
                return pdfs[idx - 1]
        print("Invalid selection, try again.")

def get_page_number(max_pages):
    # accept CLI arg or prompt
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = input(f"Enter page number (1-{max_pages}): ").strip()
    if not arg.isdigit():
        print("Page number must be a positive integer.")
        sys.exit(1)
    pnum = int(arg)
    if pnum < 1 or pnum > max_pages:
        print(f"Page number out of range. Must be between 1 and {max_pages}.")
        sys.exit(1)
    return pnum

def extract_page_text(pdf_path: Path, page_number: int) -> str:
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"Failed to open PDF {pdf_path.name}: {e}")
        return ""
    num_pages = len(reader.pages)
    if page_number < 1 or page_number > num_pages:
        print(f"Requested page {page_number} not in range (1-{num_pages}).")
        return ""
    page = reader.pages[page_number - 1]
    text = page.extract_text()
    return text or ""

def ensure_output_txt():
    legacy_output = BASE / "output.txt"
    if not legacy_output.exists():
        try:
            legacy_output.touch()
            print(f"Created missing legacy output file: {legacy_output}")
        except Exception as e:
            print(f"Could not create legacy output.txt: {e}")
            print("The script will continue but appending to legacy output will be skipped.")

def write_user_file(page_num: int, text: str):
    out_path = BASE / f"user_input_output_file_{page_num}.txt"
    try:
        with out_path.open("w", encoding="utf-8") as f:
            header = f"----- Page {page_num} extracted -----\n\n"
            f.write(header)
            f.write(text)
            f.write("\n\n----- End -----\n")
        print(f"Wrote page {page_num} text to: {out_path}")
    except Exception as e:
        print(f"Failed to write to {out_path}: {e}")
        sys.exit(1)


def append_to_legacy_output(page_num: int, text: str, pdf_name: str):
    out = BASE / "output.txt"
    try:
        with out.open("a", encoding="utf-8") as f:
            f.write(f"\n\n--- Matches from {pdf_name} page {page_num} ---\n")
            f.write(text)
            f.write("\n\n")
        print(f"Appended extracted matches to: {out}")
    except Exception as e:
        print(f"Failed to append to legacy output {out}: {e}")
        print("If you need the legacy output file, ensure the folder is writable and try again.")

def main():
    ensure_content_folder()
    ensure_output_txt()

    cfg = load_config()
    regex_pattern = cfg.get("regex")
    if cfg and "regex" not in cfg:
        print("Configuration file found but 'regex' key is missing. The script will extract full page text.")

    # Initialize database
    db_path = BASE / "questions.db"
    conn: Connection | None = None
    try:
        conn = init_db(db_path)
        if conn is None:
            print(f"Database not available at {db_path}. DB operations will be skipped.")
        else:
            ok = ensure_table(conn)
            if not ok:
                print("Could not ensure questions table exists. DB inserts may fail.")
    except Exception as e:
        print(f"Unexpected DB initialization error: {e}")
        conn = None

    pdfs = find_pdfs()
    if not pdfs:
        print(f"No PDF files located under {BASE}. Please add PDFs to subfolders and re-run.")
        sys.exit(0)

    pdf_path = choose_pdf(pdfs)
    if pdf_path is None:
        print("No file selected. Exiting.")
        sys.exit(0)

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"Unable to read PDF {pdf_path}: {e}")
        sys.exit(1)

    max_pages = len(reader.pages)
    if max_pages == 0:
        print(f"No pages found in PDF: {pdf_path}")
        sys.exit(1)

    page_num = get_page_number(max_pages)
    text = extract_page_text(pdf_path, page_num)
    if not text:
        print(f"No text extracted from page {page_num} (may be scanned image or empty). Still writing file.")
    # If a regex is configured, extract only the matching parts
    if regex_pattern:
        matches = extract_matches(text, regex_pattern)
        if not matches:
            print("No matches found for configured regex. Writing empty result file.")
            text_to_write = ""
        else:
            # matches is a list of strings or dicts; prepare file output
            # if dict, join the question_text for output
            out_items = []
            for item in matches:
                if isinstance(item, dict):
                    out_items.append(item.get("question_text") or item.get("raw") or "")
                else:
                    out_items.append(str(item))
            text_to_write = "\n\n".join(out_items)
            # insert each match to DB if available
            if conn:
                for item in matches:
                    try:
                        if isinstance(item, dict):
                            subj = item.get("subject")
                            qtext = item.get("question_text") or item.get("raw")
                            answers = item.get("answer_options")
                            chapter = item.get("chapter")
                        elif isinstance(item, tuple) or isinstance(item, list):
                            # fallback if regex returned positional groups
                            parts = list(item)
                            # map by position: subject, question, answers, chapter
                            subj = parts[0] if len(parts) >= 4 else None
                            qtext = parts[1] if len(parts) >= 2 else (parts[0] if len(parts) >= 1 else None)
                            answers = parts[2] if len(parts) >= 3 else None
                            chapter = parts[3] if len(parts) >= 4 else None
                        else:
                            subj = None
                            qtext = str(item)
                            answers = None
                            chapter = None

                        success = insert_question(conn, pdf_path.name, page_num, qtext or "", answers, subj, chapter)
                        if not success:
                            print(f"Failed to insert question for page {page_num} into DB.")
                    except Exception as e:
                        print(f"DB error inserting question: {e}")
    else:
        text_to_write = text

    write_user_file(page_num, text_to_write)
    # Also append to legacy output.txt for convenience
    append_to_legacy_output(page_num, text_to_write, pdf_path.name)

    if conn:
        try:
            close_db(conn)
        except Exception:
            pass

if __name__ == "__main__":
    main()

#** project 5 : Create a databased to store the PDF file name, page number and the extracted text from the PDF file

