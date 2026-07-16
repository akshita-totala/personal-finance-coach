from parser.pdf_reader import extract_text_from_pdf

pdf_path = "../sample_data/sample.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)