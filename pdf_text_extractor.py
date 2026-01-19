"""
PDF Text Extractor - MVP Tool
A simple desktop application to extract text from PDF files.

Features:
- Upload PDF files via file browser
- Extract and display text from all pages
- Save extracted text to .txt file
- Simple and clean Tkinter UI
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import os
from pypdf import PdfReader


class PDFTextExtractorApp:
    """Main application class for PDF text extraction tool."""
    
    def __init__(self, root):
        """Initialize the application with UI components."""
        self.root = root
        self.root.title("PDF Text Extractor")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.current_pdf_path = None
        self.extracted_text = ""
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create and layout all UI components."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title Label
        title_label = ttk.Label(
            main_frame, 
            text="PDF Text Extractor", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Browse PDF Button
        self.browse_btn = ttk.Button(
            button_frame,
            text="📁 Browse PDF",
            command=self.browse_pdf,
            width=15
        )
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Save Text Button
        self.save_btn = ttk.Button(
            button_frame,
            text="💾 Save Text",
            command=self.save_text,
            width=15,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_text,
            width=15,
            state=tk.DISABLED
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = ttk.Label(
            button_frame,
            text="No file selected",
            foreground="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Text Display Area
        text_frame = ttk.LabelFrame(main_frame, text="Extracted Text", padding="5")
        text_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Scrolled Text Widget
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 10)
        )
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Footer
        footer_label = ttk.Label(
            main_frame,
            text="Select a PDF file to extract text",
            font=("Arial", 9),
            foreground="gray"
        )
        footer_label.grid(row=3, column=0, pady=(5, 0))
        
    def browse_pdf(self):
        """Open file dialog to select a PDF file and extract text."""
        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_pdf_path = file_path
            self.extract_text(file_path)
    
    def extract_text(self, pdf_path):
        """Extract text from the selected PDF file."""
        try:
            # Update status
            filename = os.path.basename(pdf_path)
            self.status_label.config(text=f"Processing: {filename}", foreground="blue")
            self.root.update()
            
            # Extract text using pypdf
            reader = PdfReader(pdf_path)
            extracted_text = []
            
            # Extract text from all pages
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text.strip():
                    extracted_text.append(f"--- Page {page_num} ---\n{text}\n")
            
            # Combine all text
            self.extracted_text = "\n".join(extracted_text)
            
            # Display in text area
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, self.extracted_text)
            
            # Update status and enable buttons
            page_count = len(reader.pages)
            self.status_label.config(
                text=f"✓ Extracted from {filename} ({page_count} pages)",
                foreground="green"
            )
            self.save_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.NORMAL)
            
            # Show success message
            messagebox.showinfo(
                "Success",
                f"Successfully extracted text from {page_count} page(s)!"
            )
            
        except Exception as e:
            # Handle errors
            error_msg = f"Error extracting text: {str(e)}"
            self.status_label.config(text="❌ Extraction failed", foreground="red")
            messagebox.showerror("Error", error_msg)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, f"Error: {error_msg}")
    
    def save_text(self):
        """Save extracted text to a .txt file."""
        if not self.extracted_text:
            messagebox.showwarning("Warning", "No text to save!")
            return
        
        # Open save dialog
        file_path = filedialog.asksaveasfilename(
            title="Save extracted text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.extracted_text)
                
                messagebox.showinfo(
                    "Success",
                    f"Text saved successfully to:\n{file_path}"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to save file:\n{str(e)}"
                )
    
    def clear_text(self):
        """Clear the text area and reset the application."""
        self.text_area.delete(1.0, tk.END)
        self.extracted_text = ""
        self.current_pdf_path = None
        self.status_label.config(text="No file selected", foreground="gray")
        self.save_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PDFTextExtractorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
