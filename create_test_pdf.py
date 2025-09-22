#!/usr/bin/env python3
"""
Create a simple test PDF for testing the Streamlit app
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_test_pdf():
    """Create a simple test PDF file."""
    filename = "test_document.pdf"
    
    # Create PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Test Document for OpenAI Analysis")
    
    # Add content
    c.setFont("Helvetica", 12)
    content = [
        "This is a test PDF document created for testing the OpenAI file reader.",
        "",
        "Key Features:",
        "• PDF text extraction",
        "• AI-powered analysis",
        "• Question answering",
        "",
        "The OpenAI API can now read and analyze PDF files through the Streamlit interface.",
        "Users can upload PDF documents and ask specific questions about their content.",
        "",
        "This demonstrates the capability to process various document formats including:",
        "- PDF files",
        "- Word documents (.docx)",
        "- Text files (.txt)",
        "- Code files (.py, .js, .html, etc.)",
        "",
        "The system extracts text from these documents and uses OpenAI's GPT models",
        "to provide intelligent analysis and answer user questions."
    ]
    
    y_position = height - 150
    for line in content:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    # Save PDF
    c.save()
    
    print(f"✅ Test PDF created: {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")
    return filename

if __name__ == "__main__":
    try:
        create_test_pdf()
    except ImportError:
        print("❌ reportlab not installed. Installing...")
        os.system("pip install reportlab")
        create_test_pdf()


