from pathlib import Path
from pptx import Presentation
from .styles import StyleGenerator
from .animations import AnimationHandler
from .tables import TableHandler
import base64
from io import BytesIO
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.dml import MSO_THEME_COLOR_INDEX
import math
import logging
from jinja2 import Template

logger = logging.getLogger(__name__)

class PowerPointConverter:
    def __init__(self):
        """אתחול הממיר"""
        self.style_generator = StyleGenerator()
        self.animation_handler = AnimationHandler()
        self.table_handler = TableHandler()
        self.animation_step = 0

    def _add_animation_to_element(self, element_id, shape_index, slide_index):
        """הוספת אנימציה לאלמנט"""
        animation = self.animation_handler.create_animation(
            effect_type='FADE',  # ברירת מחדל
            step=shape_index,    # כל צורה תופיע בשלב נפרד
            delay=0.2 * shape_index,  # דיליי הדרגתי
            duration=1.0
        )
        return animation

    def convert(self, pptx_path, output_path=None):
        """
        ממיר מצגת PowerPoint לקובץ HTML
        
        Args:
            pptx_path (str): נתיב לקובץ PowerPoint
            output_path (str, optional): נתיב לשמירת קובץ ה-HTML. אם לא צוין, ישמר באותה תיקייה
        
        Returns:
            str: נתיב לקובץ ה-HTML שנוצר
        """
        try:
            presentation = Presentation(pptx_path)
            html_content = self._convert_presentation(presentation)
            
            if output_path is None:
                # שמירה באותה תיקייה כמו קובץ המקור
                output_path = str(Path(pptx_path).with_suffix('.html'))
                
            # שמירת הקובץ
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            return output_path
            
        except Exception as e:
            raise Exception(f"שגיאה בהמרת המצגת: {str(e)}")
        
    def _convert_presentation(self, presentation):
        """ממיר את המצגת כולה ל-HTML"""
        slides_html = []
        for i, slide in enumerate(presentation.slides):
            slide_html = self._convert_slide(slide, i)
            slides_html.append(slide_html)

        # יצירת ה-HTML המלא
        html = self._generate_html_template(slides_html)
        return html
    
    def _generate_html_template(self, slides):
        """יוצר את תבנית ה-HTML הבסיסית"""
        title = "מצגת PowerPoint"
        styles = self.style_generator.get_base_css()
        javascript = self._generate_javascript(slides)
        total_slides = len(slides)
        
        template_str = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        {{ styles }}
    </style>
</head>
<body>
    <div class="menu-container">
        <div class="controls">
            <button id="toggleTheme">מצב כהה/בהיר</button>
            <div class="font-size-controls">
                <button id="increaseFontSize">A+</button>
                <button id="decreaseFontSize">A-</button>
            </div>
        </div>
        <div class="thumbnails">
            {% for slide in slides %}
            <div class="thumbnail" data-slide="{{ loop.index0 }}">
                <img src="{{ slide.thumbnail }}" alt="שקופית {{ loop.index }}">
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="main-content">
        <div class="presentation-container">
            <div class="slides">
                {% for slide in slides %}
                <div class="slide" id="slide-{{ loop.index0 }}" {% if not loop.first %}style="display: none;"{% endif %}>
                    {{ slide.html }}
                </div>
                {% endfor %}
            </div>
            <div class="navigation">
                <button id="prevSlide">הקודם</button>
                <span id="slideCounter">שקופית <span id="currentSlide">1</span> מתוך {{ total_slides }}</span>
                <button id="nextSlide">הבא</button>
            </div>
        </div>
    </div>

    <script>
        {{ javascript }}
    </script>
</body>
</html>
"""
        template = Template(template_str)
        context = {
            'title': title,
            'styles': styles,
            'javascript': javascript,
            'slides': slides,
            'total_slides': total_slides
        }
        return template.render(**context)
    
    def _generate_javascript(self, slides):
        """יוצר את הקוד ה-JavaScript הבסיסי"""
        return """
let currentSlide = 0;
const totalSlides = %d;
const baseFontSize = 1.0;  // גודל ברירת המחדל ב-em

document.addEventListener('DOMContentLoaded', () => {
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener('click', () => {
            showSlide(index);
        });
    });
    
    const prevButton = document.getElementById('prevSlide');
    prevButton.addEventListener('click', prevSlide);
    
    const nextButton = document.getElementById('nextSlide');
    nextButton.addEventListener('click', nextSlide);
    
    const themeButton = document.getElementById('toggleTheme');
    themeButton.addEventListener('click', toggleTheme);
    
    const increaseFontSizeButton = document.getElementById('increaseFontSize');
    increaseFontSizeButton.addEventListener('click', () => changeFontSize(0.1));
    
    const decreaseFontSizeButton = document.getElementById('decreaseFontSize');
    decreaseFontSizeButton.addEventListener('click', () => changeFontSize(-0.1));
    
    showSlide(0);
});

function showSlide(n) {
    const slides = document.querySelectorAll('.slide');
    const currentSlideSpan = document.getElementById('currentSlide');
    
    if (n >= totalSlides) currentSlide = 0;
    else if (n < 0) currentSlide = totalSlides - 1;
    else currentSlide = n;
    
    slides.forEach(slide => {
        slide.style.display = 'none';
    });
    
    slides[currentSlide].style.display = 'block';
    currentSlideSpan.textContent = currentSlide + 1;
    
    // עדכון התמונה הממוזערת הפעילה
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, index) => {
        thumb.classList.toggle('active', index === currentSlide);
    });
}

function prevSlide() {
    showSlide(currentSlide - 1);
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

function changeFontSize(delta) {
    const html = document.documentElement;
    const currentSize = parseFloat(getComputedStyle(html).getPropertyValue('--base-font-size')) || baseFontSize;
    const newSize = Math.max(0.5, Math.min(2.0, currentSize + delta));  // הגבלה בין 0.5 ל-2.0
    html.style.setProperty('--base-font-size', `${newSize}em`);
    localStorage.setItem('fontSize', newSize);
}

// טעינת העדפות שמורות
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
}

const savedFontSize = localStorage.getItem('fontSize');
if (savedFontSize) {
    document.documentElement.style.setProperty('--base-font-size', `${savedFontSize}em`);
}

// הוספת תמיכה במקלדת
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'PageUp') prevSlide();
    if (e.key === 'ArrowLeft' || e.key === 'PageDown') nextSlide();
});
""" % len(slides)

    def _convert_slide(self, slide, index):
        """
        ממיר שקופית בודדת ל-HTML
        
        Args:
            slide: אובייקט השקופית
            index: מספר השקופית
            
        Returns:
            str: תוכן ה-HTML של השקופית
        """
        try:
            # יצירת מזהה ייחודי לשקופית
            slide_id = f"slide-{index + 1}"
            
            # יצירת מיכל השקופית
            slide_html = f'<div id="{slide_id}" class="slide-content">'
            
            # המרת כל הצורות והאלמנטים בשקופית
            for shape_index, shape in enumerate(slide.shapes):
                element_id = f"{slide_id}-shape-{shape_index}"
                
                if shape.has_text_frame:
                    slide_html += self._convert_text_frame(shape, element_id)
                elif shape.shape_type == 13:  # תמונה
                    slide_html += self._convert_picture(shape, element_id)
                elif hasattr(shape, 'table'):
                    slide_html += self.table_handler.convert_table(shape.table, element_id)
                else:
                    slide_html += self._convert_shape(shape, element_id)
            
            # סגירת תגיות
            slide_html += '</div>'
            return {"html": slide_html, "thumbnail": ""}
            
        except Exception as e:
            logger.error(f"שגיאה בהמרת שקופית {index + 1}: {str(e)}")
            return {"html": f'<div class="slide error">שגיאה בהמרת שקופית {index + 1}</div>', "thumbnail": ""}
        
    def _get_background_style(self, slide):
        """מחזיר את סגנון הרקע של השקופית"""
        try:
            background = slide.background
            fill = background.fill
            if fill.type is None:
                return "background-color: white;"
            
            if hasattr(fill, 'fore_color'):
                color = fill.fore_color
                if hasattr(color, 'rgb'):
                    rgb = color.rgb
                    return f"background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});"
            
            return "background-color: white;"
        except:
            return "background-color: white;"

    def _convert_text_frame(self, shape, element_id="", animation_style=""):
        """ממיר מסגרת טקסט ל-HTML"""
        if not shape.text.strip():
            return ''
            
        # המרת מיקום וגודל מEMU ל-פיקסלים
        left = shape.left / 914400 * 96  # EMU to pixels
        top = shape.top / 914400 * 96
        width = shape.width / 914400 * 96
        height = shape.height / 914400 * 96
        
        style = f"""
            position: absolute;
            left: {left:.2f}px;
            top: {top:.2f}px;
            width: {width:.2f}px;
            height: {height:.2f}px;
            {animation_style}
        """
        
        html = f'<div class="text-box" id="{element_id}" style="{style}">'
        
        # המרת הפסקאות עם עיצוב
        for paragraph in shape.text_frame.paragraphs:
            para_style = self._get_paragraph_style(paragraph)
            html += f'<p style="{para_style}">'
            
            for run in paragraph.runs:
                run_style = self._get_run_style(run)
                html += f'<span style="{run_style}">{run.text}</span>'
            
            html += '</p>'
            
        html += '</div>'
        return html

    def _get_paragraph_style(self, paragraph):
        """מחזיר את הסגנון של פסקה"""
        style_parts = ["margin: 0"]
        
        # יישור טקסט
        if paragraph.alignment is not None:
            alignment_map = {
                0: 'right',  # PP_ALIGN.LEFT in RTL
                1: 'center',
                2: 'left',   # PP_ALIGN.RIGHT in RTL
                3: 'justify'
            }
            style_parts.append(f"text-align: {alignment_map.get(paragraph.alignment, 'right')}")
        
        # מרווח בין שורות
        if paragraph.line_spacing:
            style_parts.append(f"line-height: {paragraph.line_spacing}")
            
        return "; ".join(style_parts)

    def _get_run_style(self, run):
        """מחזיר את הסגנון של קטע טקסט"""
        style_parts = []
        
        # גופן וגודל
        if run.font.name:
            style_parts.append(f"font-family: '{run.font.name}'")
        if run.font.size:
            # המרה מ-EMU ל-px
            size_px = run.font.size.pt
            style_parts.append(f"font-size: {size_px}pt")
            
        # צבע
        if run.font.color.rgb:
            rgb = run.font.color.rgb
            style_parts.append(f"color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
            
        # עיצוב טקסט
        if run.font.bold:
            style_parts.append("font-weight: bold")
        if run.font.italic:
            style_parts.append("font-style: italic")
        if run.font.underline:
            style_parts.append("text-decoration: underline")
            
        return "; ".join(style_parts)

    def _convert_picture(self, shape, element_id="", animation_style=""):
        """ממיר תמונה ל-HTML"""
        try:
            # המרת מיקום וגודל מEMU ל-פיקסלים
            left = shape.left / 914400 * 96
            top = shape.top / 914400 * 96
            width = shape.width / 914400 * 96
            height = shape.height / 914400 * 96
            
            # המרת התמונה ל-base64
            image = shape.image
            image_bytes = image.blob
            image_base64 = base64.b64encode(image_bytes).decode()
            content_type = image.content_type or 'image/png'
            
            style = f"""
                position: absolute;
                left: {left:.2f}px;
                top: {top:.2f}px;
                width: {width:.2f}px;
                height: {height:.2f}px;
                object-fit: contain;
                {animation_style}
            """
            
            return f'''
                <img 
                    class="image" 
                    id="{element_id}" 
                    src="data:{content_type};base64,{image_base64}"
                    style="{style}"
                    alt="תמונה במצגת"
                />
            '''
        except Exception as e:
            print(f"שגיאה בהמרת תמונה: {str(e)}")
            return ''

    def _convert_shape(self, shape, element_id="", animation_style=""):
        """ממיר צורה ל-HTML"""
        # המרת מיקום וגודל מEMU ל-פיקסלים
        left = shape.left / 914400 * 96
        top = shape.top / 914400 * 96
        width = shape.width / 914400 * 96
        height = shape.height / 914400 * 96
        
        # חילוץ צבע הרקע
        fill_color = "transparent"
        if hasattr(shape.fill, 'fore_color') and shape.fill.fore_color:
            color = shape.fill.fore_color
            if hasattr(color, 'rgb'):
                rgb = color.rgb
                fill_color = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
        
        # חילוץ צבע המסגרת
        border_color = "none"
        border_width = "0"
        if shape.line:
            if hasattr(shape.line, 'color') and shape.line.color:
                color = shape.line.color
                if hasattr(color, 'rgb'):
                    rgb = color.rgb
                    border_color = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
            if hasattr(shape.line, 'width'):
                border_width = f"{shape.line.width / 914400 * 96:.2f}px"
        
        style = f"""
            position: absolute;
            left: {left:.2f}px;
            top: {top:.2f}px;
            width: {width:.2f}px;
            height: {height:.2f}px;
            background-color: {fill_color};
            border: {border_width} solid {border_color};
            border-radius: {self._get_shape_radius(shape)};
            {animation_style}
        """
        
        return f'<div class="shape" id="{element_id}" style="{style}"></div>'

    def _get_shape_radius(self, shape):
        """מחזיר את רדיוס הפינות של הצורה"""
        try:
            # אם זה מלבן מעוגל
            if hasattr(shape, 'adjustment_values') and shape.adjustment_values:
                return min(shape.width, shape.height) * shape.adjustment_values[0] / 100000
        except:
            pass
        return 0
