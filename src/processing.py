# src/processing.py
import fitz  # PyMuPDF
import re
from collections import Counter

def get_font_styles(doc):
    """
    Analyzes the entire document to find all unique font sizes and names.
    This helps us create a style profile of the document.
    """
    styles = {}
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Round the font size to handle minor variations
                        size = round(span["size"])
                        if size not in styles:
                            styles[size] = []
                        # Store the font name (e.g., 'Arial-Bold')
                        styles[size].append(span["font"])
    
    # Return a dictionary of {size: [font_name, font_name,...]}
    return styles

def get_heading_levels(font_styles):
    """
    Determines which font sizes correspond to H1, H2, H3, and Title
    based on their descending size.
    """
    # Get all unique font sizes and sort them from largest to smallest
    sorted_sizes = sorted(font_styles.keys(), reverse=True)
    
    levels = {}
    if not sorted_sizes:
        return levels, None

    # The largest font size is assumed to be the Title
    title_size = sorted_sizes[0]
    
    # The next three largest unique sizes are H1, H2, H3
    heading_sizes = sorted_sizes[1:]
    if len(heading_sizes) > 0:
        levels[heading_sizes[0]] = "H1"
    if len(heading_sizes) > 1:
        levels[heading_sizes[1]] = "H2"
    if len(heading_sizes) > 2:
        levels[heading_sizes[2]] = "H3"
        
    return levels, title_size

def extract_outline_from_pdf(pdf_path):
    """
    Main function to extract the title and a hierarchical outline (H1, H2, H3)
    from a PDF document.
    """
    doc = fitz.open(pdf_path)
    
    # Step 1: Profile the document's font styles and determine heading levels
    font_styles = get_font_styles(doc)
    heading_levels, title_size = get_heading_levels(font_styles)
    
    title = ""
    outline = []
    
    # Find the title first (usually on the first page)
    first_page_blocks = doc[0].get_text("dict")["blocks"]
    for block in first_page_blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if round(span["size"]) == title_size:
                        # Clean up the title text
                        title_text = " ".join(title.split())
                        if not title: # Take the first instance as the title
                           title = span["text"].strip()

    # Step 2: Iterate through the document to extract headings
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                # A heading is usually a single line in a block
                if len(block["lines"]) == 1:
                    line = block["lines"][0]
                    if len(line["spans"]) == 1:
                        span = line["spans"][0]
                        font_size = round(span["size"])
                        
                        # Check if this font size corresponds to a heading level
                        if font_size in heading_levels:
                            heading_text = span["text"].strip()
                            # Ignore very short or non-alphanumeric text (like page numbers)
                            if len(heading_text) > 2 and re.search('[a-zA-Z]', heading_text):
                                outline.append({
                                    "level": heading_levels[font_size],
                                    "text": heading_text,
                                    "page": page_num + 1
                                })

    # If no title was found with the largest font, use the first H1
    if not title and outline:
        title = outline[0]["text"]
        
    # Construct the final JSON output
    result = {
        "title": title,
        "outline": outline
    }
    
    return result
