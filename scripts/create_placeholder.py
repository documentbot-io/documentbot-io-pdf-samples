#!/usr/bin/env python3
"""
Create a placeholder PDF for Google translation failure
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_placeholder_pdf(output_path, message="Google cannot translate scanned PDFs"):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Center the text
    c.setFont("Helvetica", 24)
    text_width = c.stringWidth(message, "Helvetica", 24)
    x = (width - text_width) / 2
    y = height / 2
    
    c.drawString(x, y, message)
    
    # Add smaller note below
    c.setFont("Helvetica", 12)
    note = "This is a placeholder for translation testing"
    note_width = c.stringWidth(note, "Helvetica", 12)
    x_note = (width - note_width) / 2
    c.drawString(x_note, y - 30, note)
    
    c.save()
    print(f"Created placeholder PDF: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = "placeholder.pdf"
    
    message = sys.argv[2] if len(sys.argv) > 2 else "Google cannot translate scanned PDFs"
    create_placeholder_pdf(output, message)