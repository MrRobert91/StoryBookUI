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
        # OpenDyslexic Font registration
        font_reg_path = os.path.join(STATIC_DIR, "OpenDyslexic-Regular.otf")
        font_bold_path = os.path.join(STATIC_DIR, "OpenDyslexic-Bold.otf")

        if os.path.exists(font_reg_path):
            self.add_font("OpenDyslexic", "", font_reg_path)
        else:
            print(f"Warning: OpenDyslexic-Regular not found at {font_reg_path}")

        if os.path.exists(font_bold_path):
            self.add_font("OpenDyslexic", "B", font_bold_path)
        else:
            print(f"Warning: OpenDyslexic-Bold not found at {font_bold_path}")

    def add_page(self, *args, **kwargs):
        super().add_page(*args, **kwargs)
        # 1. Background: purple-50 (RGB 250, 245, 255)
        self.set_fill_color(250, 245, 255)
        self.rect(0, 0, self.w, self.h, style='F')

        # 2. Decorative Border: Black
        self.set_draw_color(0, 0, 0)
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
        try:
            self.set_font('OpenDyslexic', '', 8)
        except:
            self.set_font('Helvetica', '', 8)
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
    
    # Title Typography: OpenDyslexic Bold, with white background box and black border
    try:
        pdf.set_font('OpenDyslexic', 'B', 36)
    except:
        pdf.set_font('Helvetica', 'B', 36)

    h_line = 20
    # Calculate height for rounded rectangle
    lines = pdf.multi_cell(0, h_line, title, align='C', split_only=True)
    total_h = len(lines) * h_line

    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(2.5)
    
    # Draw rounded rectangle for title background
    pdf.rect(pdf.get_x(), pdf.get_y(), pdf.w - 2 * pdf.l_margin, total_h, style='FD', round_corners=True, corner_radius=10)

    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, h_line, title, border=0, align='C')

    # Reset text styles
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

                # Draw black frame around the image
                pdf.set_draw_color(0, 0, 0)
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
                    pdf.set_font('OpenDyslexic', 'B', 24)
                except:
                    pdf.set_font('Helvetica', 'B', 24)

                h_line = 15
                lines = pdf.multi_cell(0, h_line, chap_title, align='C', split_only=True)
                total_h = len(lines) * h_line

                pdf.set_fill_color(255, 255, 255)
                pdf.set_draw_color(0, 0, 0)
                pdf.set_line_width(2.5)

                # Draw rounded rectangle for chapter title
                pdf.rect(pdf.get_x(), pdf.get_y(), pdf.w - 2 * pdf.l_margin, total_h, style='FD', round_corners=True, corner_radius=8)

                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, h_line, chap_title, border=0, align='C')

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

                        # Black Frame
                        pdf.set_draw_color(0, 0, 0)
                        pdf.set_line_width(1)
                        pdf.rect(x_pos - 0.5, y_start - 0.5, w_img + 1, h_img + 1, style='D', round_corners=True, corner_radius=8)
                        pdf.set_y(y_start + h_img + 10)
                except Exception as e:
                    print(f"Error embedding chapter image: {e}")
            
            # Chapter Text
            try:
                pdf.set_font('OpenDyslexic', '', 17)
            except:
                pdf.set_font('Helvetica', '', 17)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 11, chap_text)
            
    # --- Last Page Branding ---
    branding_text = "Make yours in cuentee"
    h_box = 21 # 50% larger than 14
    w_box = 170 # Leaving 20mm margin on each side (210 - 40)
    start_x = 20
    favicon_w = 12 # Scaled up
    spacing = 5

    # Move to a safe position at the bottom area if there's space, or let it trigger a new page
    if pdf.get_y() < pdf.h - 50:
        pdf.set_y(-40) # Position near bottom
    elif pdf.get_y() + h_box + 10 > pdf.page_break_trigger:
        pdf.add_page()
    else:
        pdf.ln(10)

    y_pos = pdf.get_y()

    try:
        pdf.set_font('OpenDyslexic', 'B', 24)
    except:
        pdf.set_font('Helvetica', 'B', 24)

    text_w = pdf.get_string_width(branding_text)
    content_w = text_w + spacing + favicon_w
    padding_x = (w_box - content_w) / 2

    # Draw Box: Intermediate purple (Purple-300), Black border, Rounded corners
    pdf.set_fill_color(216, 180, 254)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(2.0)
    pdf.rect(start_x, y_pos, w_box, h_box, style='FD', round_corners=True, corner_radius=5)

    # Add link to the whole box area
    pdf.link(start_x, y_pos, w_box, h_box, 'https://www.cuentee.com/')

    # Place Text (Black)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(start_x + padding_x, y_pos)
    pdf.cell(text_w, h_box, branding_text, border=0, ln=0, align='L')

    # Place Favicon (after text, centered vertically in box)
    favicon_path = os.path.join(STATIC_DIR, "favicon.png")
    if os.path.exists(favicon_path):
        pdf.image(favicon_path, x=start_x + padding_x + text_w + spacing, y=y_pos + (h_box - favicon_w)/2, w=favicon_w)

    # Output to bytes
    return bytes(pdf.output())
