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

import requests

def generate_story_pdf(story_data: dict) -> bytes:
    """
    Generates a PDF from the story data.
    
    Args:
        story_data (dict): Dictionary with 'title' and 'chapters' list.
                           Each chapter is a dict with 'title' and 'text' (or 'content').
    
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
    pdf.ln(10)

    # 1. Cover Image (if exists)
    cover_url = story_data.get("cover_image_url")
    if cover_url:
        try:
            # Fetch image
            response = requests.get(cover_url, timeout=10)
            if response.status_code == 200:
                img_data = io.BytesIO(response.content)
                # Calculate width to center it (approx 100mm wide)
                x_pos = (210 - 100) / 2
                pdf.image(img_data, x=x_pos, w=100)
                pdf.ln(10)
        except Exception as e:
            print(f"Error embedding cover image: {e}")
            # Continue without image
            pass
            
    pdf.ln(10)
    
    # Chapters
    chapters = story_data.get("chapters", [])
    
    # Ensure chapters is a list
    if not isinstance(chapters, list):
        if isinstance(chapters, str):
             pass 
        chapters = []

    for chapter in chapters:
        if isinstance(chapter, dict):
            # Keys might be 'title' and 'text' or 'content'
            chap_title = chapter.get("title", "")
            chap_text = chapter.get("content") or chapter.get("text", "")
            chap_image_url = chapter.get("image_url")
            
            # Add a new page for each chapter start? Optional. 
            # Let's just create space.
            if pdf.get_y() > 250: # Check for page break
                pdf.add_page()
            
            if chap_title:
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(0, 10, chap_title, 0, 1, 'L')
                pdf.ln(5)
            
            # Chapter Image
            if chap_image_url:
                try:
                    resp = requests.get(chap_image_url, timeout=10)
                    if resp.status_code == 200:
                        c_img = io.BytesIO(resp.content)
                        # Center image, width 80mm
                        x_pos = (210 - 80) / 2
                        pdf.image(c_img, x=x_pos, w=80)
                        pdf.ln(5)
                except Exception as e:
                    print(f"Error embedding chapter image: {e}")
            
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
