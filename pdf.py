from fpdf import FPDF
import os

# Ensure output directory exists
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Create a sample PDF file with some text content
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sample PDF for MetaMind Testing', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)

sample_text = '''
MetaMind is an automated metadata generation system that uses NLP to extract meaningful information from documents.

This sample PDF file is created to test the text extraction and metadata generation capabilities of the system.

It contains multiple paragraphs, key phrases, and named entities like OpenAI, Python, and Streamlit.

Enjoy testing!
'''

pdf.multi_cell(0, 10, sample_text)

file_path = os.path.join(output_dir, 'sample_test.pdf')
pdf.output(file_path)

print(f"Sample PDF created at: {file_path}")
