# exports.py
import pandas as pd
from fpdf import FPDF
from io import BytesIO

def export_to_csv(rows, path):
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)

def export_to_json(rows, path):
    df = pd.DataFrame(rows)
    df.to_json(path, orient="records", date_format="iso")

def export_to_pdf(rows):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for r in rows:
        pdf.multi_cell(0, 6, txt=str(r))
    return pdf.output(dest="S").encode("latin-1")