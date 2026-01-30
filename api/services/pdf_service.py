import os
import io
import requests
from fpdf import FPDF
from fpdf.enums import TextMode
from PIL import Image, ImageDraw, ImageEnhance

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

def get_faded_bg_image(opacity=0.5):
    """
    Loads pdf_bg.png, reduces opacity, and returns bytes.
    """
    bg_path = os.path.join(STATIC_DIR, "pdf_bg.png")
    if not os.path.exists(bg_path):
        return None
    
    try:
        img = Image.open(bg_path).convert("RGBA")
        
        # Reduce opacity
        alpha = img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        img.putalpha(alpha)
        
        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        return output
    except Exception as e:
        print(f"Error processing background image: {e}")
        return None

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

        # 1b. Image Background (Faded)
        bg_stream = get_faded_bg_image(opacity=0.5)
        if bg_stream:
            self.image(bg_stream, x=0, y=0, w=self.w, h=self.h)

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
    
    # Title Typography
    # Title Typography
    title_font_size = 32
    if len(title) > 23:
        title_font_size -= 4

    try:
        pdf.set_font('OpenDyslexic', 'B', title_font_size)
    except:
        pdf.set_font('Helvetica', 'B', title_font_size)

    h_line = 10  # Reduced line spacing by 50%
    # Calculate height for rounded rectangle
    lines = pdf.multi_cell(0, h_line, title, align='C', split_only=True)
    text_h = len(lines) * h_line
    padding_v = text_h * 0.25  # 50% extra margin (25% top + 25% bottom)
    total_h = text_h + (padding_v * 2)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(2.5)
    
    # Draw rounded rectangle for title background
    # Use full width available (w - 2*margin)
    available_w = pdf.w - 2 * pdf.l_margin
    rect_y = pdf.get_y()
    pdf.rect(pdf.l_margin, rect_y, available_w, total_h, style='FD', round_corners=True, corner_radius=10)

    pdf.set_text_color(0, 0, 0)
    pdf.set_y(rect_y + padding_v)  # Move text down by padding
    pdf.multi_cell(0, h_line, title, border=0, align='C')
    pdf.set_y(rect_y + total_h)  # Position after the box

    # Reset text styles
    pdf.set_line_width(0.2)
    pdf.ln(15)

    # Cover Image
    cover_url = story_data.get("cover_image_url")
    if cover_url:
        try:
            response = requests.get(cover_url, timeout=10)
            if response.status_code == 200:
                # Rounded image with radius
                rounded_img = get_rounded_image(response.content, radius=80)
                img_stream = io.BytesIO(rounded_img)

                # Full width (210 - 40 = 170mm)
                w_img = 170 
                x_pos = pdf.l_margin # 20mm

                y_start = pdf.get_y()
                # Place image
                info = pdf.image(img_stream, x=x_pos, w=w_img)
                h_img = info.rendered_height

                # Draw black frame
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
                chap_title_font_size = 24
                if len(chap_title) > 23:
                    chap_title_font_size -= 4

                try:
                    pdf.set_font('OpenDyslexic', 'B', chap_title_font_size)
                except:
                    pdf.set_font('Helvetica', 'B', chap_title_font_size)

                h_line = 7.5  # Reduced line spacing by 50%
                lines = pdf.multi_cell(0, h_line, chap_title, align='C', split_only=True)
                text_h = len(lines) * h_line
                padding_v = text_h * 0.25  # 50% extra margin (25% top + 25% bottom)
                total_h = text_h + (padding_v * 2)

                pdf.set_fill_color(255, 255, 255)
                pdf.set_draw_color(0, 0, 0)
                pdf.set_line_width(2.5)

                # Full width
                rect_y = pdf.get_y()
                pdf.rect(pdf.l_margin, rect_y, available_w, total_h, style='FD', round_corners=True, corner_radius=8)

                pdf.set_text_color(0, 0, 0)
                pdf.set_y(rect_y + padding_v)  # Move text down by padding
                pdf.multi_cell(0, h_line, chap_title, border=0, align='C')
                pdf.set_y(rect_y + total_h)  # Position after the box
                pdf.ln(10)
            
            # Chapter Image
            if chap_image_url:
                try:
                    resp = requests.get(chap_image_url, timeout=10)
                    if resp.status_code == 200:
                        rounded_img = get_rounded_image(resp.content, radius=50)
                        img_stream = io.BytesIO(rounded_img)
                        
                        # Full Width
                        w_img = 170
                        x_pos = pdf.l_margin

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
                pdf.set_font('OpenDyslexic', '', 18)
            except:
                pdf.set_font('Helvetica', '', 18)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, chap_text) # Increased line height for 18pt font
            
    # --- Last Page: Call to Action ---
    pdf.add_page()
    
    # Vertically center content approximately
    # Page height ~297mm. Content height estimate:
    # Title (20) + Image (80) + Text (20) = 120mm
    # Start Y approx 60mm
    pdf.set_y(60)

    # 1. Big Logo Image
    logo_path = os.path.join(STATIC_DIR, "logo_cta.png")
    if os.path.exists(logo_path):
        # Center logo, maybe 80mm wide? User said "imagen como logo en grande"
        w_logo = 100
        x_logo = (210 - w_logo) / 2
        pdf.image(logo_path, x=x_logo, w=w_logo)
        pdf.ln(10)

    pdf.ln(10)

    # 2. CTA Box
    cta_text = "Create your own custom stories with Cuentee"
    cta_link = "https://www.cuentee.com/"

    try:
        pdf.set_font('OpenDyslexic', 'B', 24)
    except:
        pdf.set_font('Helvetica', 'B', 24)

    # Calculate text width/height
    # We want a big box. Let's make it full width (170mm).
    box_w = 170
    box_x = 20
    
    # Draw logic similar to title
    pdf.set_fill_color(126, 34, 206) # Purple-700
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(2.0)
    
    # MultiCell to calculate height
    lines = pdf.multi_cell(box_w, 15, cta_text, align='C', split_only=True)
    box_h = (len(lines) * 15) + 20 # Add padding
    
    # Draw Box background
    # Use link on the rect? FPDF link is usually on cell/image. 
    # We can add a link over the area.
    pdf.rect(box_x, pdf.get_y(), box_w, box_h, style='FD', round_corners=True, corner_radius=15)
    
    # Add Link coverage
    pdf.link(box_x, pdf.get_y(), box_w, box_h, cta_link)

    # Add Text inside
    pdf.set_text_color(255, 255, 255)
    # Move cursor inside padding
    pdf.set_y(pdf.get_y() + 10) 
    pdf.set_x(box_x)
    pdf.multi_cell(box_w, 15, cta_text, border=0, align='C')

    # Output to bytes
    return bytes(pdf.output())
