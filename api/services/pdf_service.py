from fpdf import FPDF
import io

class StoryPDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'StoryBook', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_story_pdf(story_data: dict) -> bytes:
    """
    Generates a PDF from the story data.
    
    Args:
        story_data (dict): Dictionary with 'title' and 'chapters' list.
                           Each chapter is a dict with 'title' and 'text'.
    
    Returns:
        bytes: The generated PDF content.
    """
    pdf = StoryPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Story Title
    title = story_data.get("title", "Untitled Story")
    pdf.set_font('Arial', 'B', 24)
    pdf.multi_cell(0, 10, title, align='C')
    pdf.ln(20)
    
    # Chapters
    chapters = story_data.get("chapters", [])
    
    # Ensure chapters is a list
    if not isinstance(chapters, list):
        if isinstance(chapters, str):
             # Try to parse if it's a string, or just print it as content
             pass 
        chapters = []

    for chapter in chapters:
        # Chapter Title
        if isinstance(chapter, dict):
            chap_title = chapter.get("title", "")
            chap_text = chapter.get("text", "")
            
            if chap_title:
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(0, 10, chap_title, 0, 1, 'L')
                pdf.ln(5)
            
            # Chapter Text
            pdf.set_font('Times', '', 12)
            pdf.multi_cell(0, 8, chap_text)
            pdf.ln(10)
            
    # Output to bytes
    try:
        output = pdf.output(dest='S')
        # Supabase storage client usually expects exact bytes, not bytearray
        return bytes(output)
    except TypeError:
        # Fallback for older fpdf2 versions or different behaviors
        return pdf.output(dest='S').encode('latin-1') 
    except Exception:
        # FPDF2 usually returns bytes with dest='S' but let's be safe
        buffer = io.BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()
