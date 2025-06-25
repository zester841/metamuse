from fpdf import FPDF
import os
from datetime import datetime

# Ensure output directory exists
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

class EssayPDF(FPDF):
    def header(self):
        self.set_font('Times', 'B', 14)
        self.cell(0, 10, 'Reflections on a Changing City', 0, 1, 'C')
        self.set_font('Times', 'I', 10)
        self.cell(0, 10, 'By Priya Menon    |    May 2025', 0, 1, 'C')
        self.line(10, 25, 200, 25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Times', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def section_body(self, body):
        self.set_font('Times', '', 12)
        self.multi_cell(0, 8, body)
        self.ln()

pdf = EssayPDF()
pdf.alias_nb_pages()
pdf.add_page()

# Abstract
pdf.set_font('Times', 'B', 12)
pdf.cell(0, 10, 'Abstract', 0, 1)
pdf.set_font('Times', '', 12)
abstract = (
    "This essay explores the transformation of a mid-sized Indian city over the past two decades, "
    "focusing on the interplay between tradition and modernity. Through personal observations, "
    "conversations with residents, and reflections on public spaces, the essay examines how urban life, "
    "community bonds, and individual aspirations have evolved in the face of rapid economic and social change."
)
pdf.multi_cell(0, 8, abstract)
pdf.ln(4)

# Table of Contents
pdf.set_font('Times', 'B', 12)
pdf.cell(0, 10, 'Contents', 0, 1)
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
    pdf.cell(0, 8, item, 0, 1)
pdf.ln(4)

# Section 1
pdf.section_title("1. Introduction")
pdf.section_body(
    "Cities are living entities, always in flux. Over the last twenty years, my hometown of Suryanagar has become a microcosm of India's transformation. "
    "Once a quiet town known for its ancient banyan trees and narrow lanes, it now pulses with new energy. The skyline is dotted with glass towers, and the sounds of construction mingle with the calls of street vendors. "
    "Yet, beneath this surface, the essence of the city remains—rooted in the stories of its people."
)

# Section 2
pdf.section_title("2. Morning in the Old Quarter")
pdf.section_body(
    "Each morning, the old quarter awakens slowly. Elderly men gather at the tea stalls, discussing politics and cricket, while women in colorful saris sweep the thresholds of their homes. The aroma of fresh idlis and filter coffee drifts through the air. "
    "Children in uniforms hurry past, their laughter echoing off the faded walls. Despite the growing presence of supermarkets and malls, the local grocer still greets every customer by name."
)

# Section 3
pdf.section_title("3. The Marketplace and New Voices")
pdf.section_body(
    "The central marketplace has always been the heart of Suryanagar. In recent years, new voices have joined the chorus—young entrepreneurs selling handmade soaps, a group of students running a weekend book exchange, migrant workers offering regional snacks. "
    "The old and new coexist, sometimes in harmony, sometimes in tension. A fruit vendor, whose family has worked the same stall for generations, now competes with online delivery services. "
    "Yet, on festival days, the market still becomes a riot of color and sound, drawing crowds from every corner of the city."
)

# Section 4
pdf.section_title("4. Changing Neighborhoods")
pdf.section_body(
    "Neighborhoods that were once tightly knit have begun to change. Apartment complexes rise where single-story homes once stood. Gated communities promise security and convenience, but sometimes at the cost of neighborly warmth. "
    "Some lament the loss of open spaces and familiar faces, while others embrace the opportunities that come with new infrastructure and connectivity. "
    "In the evenings, parks fill with joggers, grandparents, and teenagers glued to their phones—a tapestry of old habits and new routines."
)

# Section 5
pdf.section_title("5. Festivals and Memory")
pdf.section_body(
    "Festivals remain the thread that binds the city together. During Diwali, the streets shimmer with lights, and families share sweets across generations. Eid brings the aroma of biryani and the sound of laughter spilling from open windows. "
    "Even as traditions evolve—rangoli patterns inspired by Instagram, or digital invitations replacing handwritten notes—the spirit of celebration endures. "
    "For many, these moments are a bridge to the past, a way of remembering who we are, even as we change."
)

# Section 6
pdf.section_title("6. Hopes for Tomorrow")
pdf.section_body(
    "As Suryanagar grows, so do the dreams of its people. Students aspire to study abroad, shopkeepers hope for steady business, and artists seek new audiences. "
    "There are challenges—traffic jams, pollution, the struggle to balance progress with preservation. But there is also resilience, creativity, and a sense of belonging that no skyscraper can overshadow. "
    "In the quiet moments, as dusk settles over the city, I am reminded that change is not the end of a story, but the beginning of a new one."
)

# Save PDF
file_path = os.path.join(output_dir, 'genuine_story_document.pdf')
pdf.output(file_path)

print(f"Genuine narrative PDF created at: {file_path}")
