# PDF Text Extractor - Quick Start Guide

## Installation

1. Install the required library:
```bash
pip install -r requirements.txt
```

## Running the Application

2. Launch the app:
```bash
python pdf_text_extractor.py
```

## Usage

1. **Browse PDF**: Click the "📁 Browse PDF" button and select your PDF file
2. **View Text**: Extracted text appears automatically in the text area
3. **Save Text**: Click "💾 Save Text" to export to a .txt file
4. **Clear**: Click "🗑️ Clear" to reset and process another PDF

## Features

- ✅ Extract text from all pages of a PDF
- ✅ Save extracted text to .txt files
- ✅ Simple, clean desktop interface
- ✅ Error handling for invalid files
- ✅ Cross-platform (Windows, macOS, Linux)

## Requirements

- Python 3.x
- pypdf library (installed via requirements.txt)
- Tkinter (comes pre-installed with Python)

## Notes

- Works with digital PDFs (text-based)
- Does not support scanned PDFs (OCR not included in MVP)
- Extracts text from all pages with page separators
