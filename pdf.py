from fpdf import FPDF
import os

def clean_latin1(text):
    text = text.replace('—', '-').replace('–', '-')
    text = text.replace('“', '"').replace('”', '"').replace("’", "'").replace("‘", "'")
    return text.encode('latin-1', 'ignore').decode('latin-1')

output_dir = 'outputs'
os.makedirs(output_dir, exist_ok=True)

class EssayPDF(FPDF):
    def header(self):
        self.set_font('Times', 'B', 14)
        self.cell(0, 10, clean_latin1('Reflections on a Changing City'), 0, 1, 'C')
        self.set_font('Times', 'I', 10)
        self.cell(0, 10, clean_latin1('By Priya Menon    |    May 2025'), 0, 1, 'C')
        self.line(10, 25, 200, 25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Times', 'B', 12)
        self.cell(0, 10, clean_latin1(title), 0, 1, 'L')
        self.ln(2)

    def section_body(self, body):
        self.set_font('Times', '', 12)
        self.multi_cell(0, 8, clean_latin1(body))
        self.ln()

pdf = EssayPDF()
pdf.alias_nb_pages()
pdf.add_page()

# Abstract
pdf.set_font('Times', 'B', 12)
pdf.cell(0, 10, clean_latin1('Abstract'), 0, 1)
pdf.set_font('Times', '', 12)
abstract = (
    "This essay explores the transformation of a mid-sized Indian city over the past two decades, "
    "focusing on the interplay between tradition and modernity. Through personal observations, "
    "conversations with residents, and reflections on public spaces, the essay examines how urban life, "
    "community bonds, and individual aspirations have evolved in the face of rapid economic and social change."
)
pdf.multi_cell(0, 8, clean_latin1(abstract))
pdf.ln(4)

# Table of Contents
pdf.set_font('Times', 'B', 12)
pdf.cell(0, 10, clean_latin1('Contents'), 0, 1)
pdf.set_font('Times', '', 12)
contents = [
    "1. Introduction",
    "2. Morning in the Old Quarter",
    "3. The Marketplace and New Voices",
    "4. Changing Neighborhoods",
    "5. Festivals and Memory",
    "6. Hopes for Tomorrow"
]
for item in contents:
    pdf.cell(0, 8, clean_latin1(item), 0, 1)
pdf.ln(4)

# Sections (repeat as needed)
pdf.section_title("1. Introduction")
pdf.section_body(
    "Cities are living entities, always in flux. Over the last twenty years, my hometown of Suryanagar has become a microcosm of India's transformation. "
    "Once a quiet town known for its ancient banyan trees and narrow lanes, it now pulses with new energy. The skyline is dotted with glass towers, and the sounds of construction mingle with the calls of street vendors. "
    "Yet, beneath this surface, the essence of the city remains-rooted in the stories of its people."
)

# ... (repeat for other sections) ...

file_path = os.path.join(output_dir, 'genuine_story_document.pdf')
pdf.output(file_path)

print(f"Genuine narrative PDF created at: {file_path}")
