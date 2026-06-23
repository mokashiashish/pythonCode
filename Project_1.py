with open('/Users/ashishmokashi/Documents/Python/content/My_Proj_1_txt.txt',mode= 'r') as projet_1_txt:
   my_new_file = projet_1_txt.read()
   print (my_new_file)
   projet_1_txt.close()

#Project 1: Extract text from PDF file and write to a text file
from PyPDF2 import PdfReader
from pathlib import Path

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


#Project 3 ************
import sys

BASE = Path("/Users/ashishmokashi/Documents/Python/content")

def ensure_content_folder():
    if not BASE.exists():
        print(f"Content folder not found: {BASE}")
        try:
            BASE.mkdir(parents=True, exist_ok=True)
            print(f"Created missing content folder: {BASE}")
        except Exception as e:
            print(f"Failed to create content folder: {e}")
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

def main():
    ensure_content_folder()
    ensure_output_txt()

    pdfs = find_pdfs()
    pdf_path = choose_pdf(pdfs)
    if pdf_path is None:
        sys.exit(1)

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
    write_user_file(page_num, text)

if __name__ == "__main__":
    main()