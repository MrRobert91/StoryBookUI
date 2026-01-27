import os
import io
import requests
from fpdf import FPDF
from fpdf.enums import TextMode
from PIL import Image, ImageDraw

# Assuming this file is in api/services/pdf_service.py
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

def get_rounded_image(img_data, radius=30):
    """
    Applies rounded corners to an image and returns PNG bytes.
    """
    try:
        img = Image.open(io.BytesIO(img_data)).convert("RGBA")

        # Create a mask for rounded corners
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        # Use provided radius or default to 10% of the smallest dimension
        r = min(img.size) // 10 if radius is None else radius
        draw.rounded_rectangle((0, 0) + img.size, radius=r, fill=255)

        # Apply mask
        img.putalpha(mask)

        output = io.BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()
    except Exception as e:
        print(f"Error rounding image: {e}")
        return img_data

class StoryPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font_path = os.path.join(STATIC_DIR, "ShortStack-Regular.ttf")
        if os.path.exists(font_path):
            self.add_font("KidFont", "", font_path)
        else:
            print(f"Warning: Font not found at {font_path}")

    def add_page(self, *args, **kwargs):
        super().add_page(*args, **kwargs)
        # 1. Background: purple-50 (RGB 250, 245, 255)
        self.set_fill_color(250, 245, 255)
        self.rect(0, 0, self.w, self.h, style='F')

        # 2. Decorative Border: purple-600 (RGB 147, 51, 234)
        self.set_draw_color(147, 51, 234)
        self.set_line_width(1.5)
        margin = 5
        # Draw a rectangle with rounded corners as a decorative frame
        self.rect(margin, margin, self.w - 2*margin, self.h - 2*margin, style='D', round_corners=True, corner_radius=5)
        self.set_line_width(0.2) # reset

    def header(self):
        # Empty header as per new requirements
        pass

    def footer(self):
        # Page Number at the bottom center
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} / {{nb}}', 0, 0, 'C')

def generate_story_pdf(story_data: dict) -> bytes:
    """
    Generates an improved PDF from the story data with better design and branding.
    """
    pdf = StoryPDF()
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- PAGE 1: Title and Cover ---
    title = story_data.get("title", "Untitled Story")
    
    pdf.ln(20)
    
    # Title Typography: KidFont, with white background box and black border
    try:
        pdf.set_font('KidFont', '', 36)
    except:
        pdf.set_font('Helvetica', 'B', 36)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(1)
    
    # Text Outline for the title
    pdf.text_mode = TextMode.FILL_STROKE
    pdf.set_text_color(255, 255, 255) # White fill for letters

    pdf.multi_cell(0, 20, title, border=1, align='C', fill=True)

    # Reset text styles
    pdf.text_mode = TextMode.FILL
    pdf.set_text_color(0, 0, 0)
    pdf.set_line_width(0.2)
    pdf.ln(15)

    # Cover Image
    cover_url = story_data.get("cover_image_url")
    if cover_url:
        try:
            response = requests.get(cover_url, timeout=10)
            if response.status_code == 200:
                rounded_img = get_rounded_image(response.content, radius=80)
                img_stream = io.BytesIO(rounded_img)

                w_img = 140
                x_pos = (210 - w_img) / 2

                y_start = pdf.get_y()
                # Place image
                info = pdf.image(img_stream, x=x_pos, w=w_img)
                h_img = info.rendered_height

                # Draw purple frame around the image
                pdf.set_draw_color(147, 51, 234)
                pdf.set_line_width(1)
                pdf.rect(x_pos - 0.5, y_start - 0.5, w_img + 1, h_img + 1, style='D', round_corners=True, corner_radius=10)
                pdf.set_y(y_start + h_img + 10)
        except Exception as e:
            print(f"Error embedding cover image: {e}")

    # Chapters
    chapters = story_data.get("chapters", [])
    if not isinstance(chapters, list):
        chapters = []

    for chapter in chapters:
        if isinstance(chapter, dict):
            pdf.add_page()
            
            chap_title = chapter.get("title", "")
            chap_text = chapter.get("content") or chapter.get("text", "")
            chap_image_url = chapter.get("image_url")
            
            # Chapter Title
            if chap_title:
                try:
                    pdf.set_font('KidFont', '', 24)
                except:
                    pdf.set_font('Helvetica', 'B', 24)

                pdf.set_fill_color(255, 255, 255)
                pdf.set_draw_color(0, 0, 0)
                pdf.set_line_width(0.8)
                pdf.text_mode = TextMode.FILL_STROKE
                pdf.set_text_color(255, 255, 255)

                pdf.multi_cell(0, 15, chap_title, border=1, align='C', fill=True)

                pdf.text_mode = TextMode.FILL
                pdf.set_text_color(0, 0, 0)
                pdf.ln(10)
            
            # Chapter Image
            if chap_image_url:
                try:
                    resp = requests.get(chap_image_url, timeout=10)
                    if resp.status_code == 200:
                        rounded_img = get_rounded_image(resp.content, radius=50)
                        img_stream = io.BytesIO(rounded_img)
                        w_img = 120
                        x_pos = (210 - w_img) / 2

                        y_start = pdf.get_y()
                        info = pdf.image(img_stream, x=x_pos, w=w_img)
                        h_img = info.rendered_height

                        # Purple Frame
                        pdf.set_draw_color(147, 51, 234)
                        pdf.set_line_width(1)
                        pdf.rect(x_pos - 0.5, y_start - 0.5, w_img + 1, h_img + 1, style='D', round_corners=True, corner_radius=8)
                        pdf.set_y(y_start + h_img + 10)
                except Exception as e:
                    print(f"Error embedding chapter image: {e}")
            
            # Chapter Text
            pdf.set_font('Helvetica', '', 14)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 8, chap_text)
            
    # --- Last Page Branding ---
    # Add branding at the bottom of the last page
    pdf.set_y(-35)
    try:
        pdf.set_font('KidFont', '', 16)
    except:
        pdf.set_font('Helvetica', 'B', 16)

    pdf.set_text_color(147, 51, 234) # Purple

    branding_text = "make yours in cuentee"
    text_w = pdf.get_string_width(branding_text)
    favicon_w = 8
    spacing = 3
    total_w = text_w + spacing + favicon_w

    start_x = (210 - total_w) / 2
    pdf.set_x(start_x)

    # Text link
    pdf.cell(text_w, 10, branding_text, 0, 0, 'L', link='https://www.cuentee.com/')

    # Favicon link
    favicon_path = os.path.join(STATIC_DIR, "favicon.png")
    if os.path.exists(favicon_path):
        # Align favicon with text
        pdf.image(favicon_path, x=start_x + text_w + spacing, y=pdf.get_y() + 1, w=favicon_w)
        # Add a link over the favicon area
        pdf.link(start_x + text_w + spacing, pdf.get_y() + 1, favicon_w, favicon_w, 'https://www.cuentee.com/')

    # Output to bytes
    return bytes(pdf.output())
