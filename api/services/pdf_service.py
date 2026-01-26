from fpdf import FPDF
import io

class StoryPDF(FPDF):
    def header(self):
        # Branding Header
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(128, 0, 128) # Purple
        self.cell(0, 10, 'made by cuentee.com', 0, 0, 'R', link='https://www.cuentee.com/')
        self.ln(15)
        # Decorative line
        self.set_draw_color(200, 200, 200)
        self.line(10, 15, 200, 15)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-20)
        # Decorative line
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} / {{nb}}', 0, 0, 'C')

import requests

def generate_story_pdf(story_data: dict) -> bytes:
    """
    Generates a PDF from the story data.
    """
    # Initialize PDF
    pdf = StoryPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- PAGE 1: Title and Cover Only ---
    
    # Title Styling
    title = story_data.get("title", "Untitled Story")
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(50, 50, 50)
    
    # Calculate height for vertical centering of cover page elements roughly
    pdf.ln(30)
    
    # Title with Border
    # MultiCell with border is tricky for centering text inside, 
    # but 'border=1' draws a box around the cell block.
    # Let's adjust color for the border
    pdf.set_draw_color(100, 0, 100) # Dark Purple border
    pdf.set_line_width(1)
    
    # We use a Cell for single line title or MultiCell if it wraps. 
    # To look like a "plaque", we can use background fill or just border.
    # Let's use a nice padding effect by drawing a cell.
    pdf.multi_cell(0, 20, title, border=1, align='C')
    pdf.set_line_width(0.2) # Reset
    pdf.ln(20)

    # Cover Image
    cover_url = story_data.get("cover_image_url")
    if cover_url:
        try:
            response = requests.get(cover_url, timeout=10)
            if response.status_code == 200:
                img_data = io.BytesIO(response.content)
                # Larger cover image
                x_pos = (210 - 140) / 2
                pdf.image(img_data, x=x_pos, w=140)
        except Exception as e:
            print(f"Error embedding cover image: {e}")
            
    # --- END PAGE 1 ---
    
    # Chapters
    chapters = story_data.get("chapters", [])
    if not isinstance(chapters, list):
        chapters = []

    for chapter in chapters:
        if isinstance(chapter, dict):
            # --- NEW PAGE FOR EACH CHAPTER ---
            pdf.add_page()
            
            chap_title = chapter.get("title", "")
            chap_text = chapter.get("content") or chapter.get("text", "")
            chap_image_url = chapter.get("image_url")
            
            # Chapter Title
            if chap_title:
                pdf.set_font('Helvetica', 'B', 22)
                pdf.set_text_color(80, 0, 80) # Dark Purple
                pdf.cell(0, 15, chap_title, 0, 1, 'C') # Centered chapter title
                pdf.ln(10)
                pdf.set_text_color(0, 0, 0)
            
            # Chapter Image
            if chap_image_url:
                try:
                    resp = requests.get(chap_image_url, timeout=10)
                    if resp.status_code == 200:
                        c_img = io.BytesIO(resp.content)
                        # Center image
                        x_pos = (210 - 120) / 2
                        pdf.image(c_img, x=x_pos, w=120)
                        pdf.ln(10)
                except Exception as e:
                    print(f"Error embedding chapter image: {e}")
            
            # Chapter Text
            # Use a slightly larger, readable font. 
            # Helvetica is standard. 'Times' is also good for reading.
            # Let's stick to Helvetica for consistency or Times for book feel.
            # User asked for "tipografia mas apropiada para cuentos". 
            # Sans-serif (Helvetica) is often easier for kids than Serif (Times).
            pdf.set_font('Helvetica', '', 14) 
            pdf.set_text_color(40, 40, 40)
            
            # Add some spacing between lines (h=8 is default-ish, let's allow more breathing room)
            pdf.multi_cell(0, 8, chap_text)
            
    # Output
    try:
        output = pdf.output(dest='S')
        return bytes(output)
    except TypeError:
        return pdf.output(dest='S').encode('latin-1') 
    except Exception:
        buffer = io.BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()
