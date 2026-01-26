from fpdf import FPDF
import io

class StoryPDF(FPDF):
    def header(self):
        # Header is left empty or minimal as requested? 
        # User said "En vez de storybook, deberia poner made by cuentee.com en morado"
        # Since "StoryBook" was in the header, we'll put the new text there.
        self.set_font('Arial', 'I', 10)
        self.set_text_color(128, 0, 128) # Purple
        # Move to right
        self.cell(0, 10, 'made by cuentee.com', 0, 0, 'R', link='https://www.cuentee.com/')
        self.ln(20)
        # Reset color
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

import requests

def generate_story_pdf(story_data: dict) -> bytes:
    """
    Generates a PDF from the story data.
    """
    pdf = StoryPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- PAGE 1: Title and Cover Only ---
    
    # Story Title
    title = story_data.get("title", "Untitled Story")
    pdf.set_font('Arial', 'B', 24)
    # Give some top margin
    pdf.ln(20) 
    pdf.multi_cell(0, 10, title, align='C')
    pdf.ln(10)

    # Cover Image
    cover_url = story_data.get("cover_image_url")
    if cover_url:
        try:
            response = requests.get(cover_url, timeout=10)
            if response.status_code == 200:
                img_data = io.BytesIO(response.content)
                # Center, larger
                x_pos = (210 - 120) / 2
                pdf.image(img_data, x=x_pos, w=120)
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
            
            if chap_title:
                pdf.set_font('Arial', 'B', 18)
                pdf.cell(0, 10, chap_title, 0, 1, 'L')
                pdf.ln(10)
            
            # Chapter Image
            if chap_image_url:
                try:
                    resp = requests.get(chap_image_url, timeout=10)
                    if resp.status_code == 200:
                        c_img = io.BytesIO(resp.content)
                        # Center image
                        x_pos = (210 - 100) / 2
                        pdf.image(c_img, x=x_pos, w=100)
                        pdf.ln(10)
                except Exception as e:
                    print(f"Error embedding chapter image: {e}")
            
            # Chapter Text
            pdf.set_font('Times', '', 12)
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
