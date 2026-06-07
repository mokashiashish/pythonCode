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
