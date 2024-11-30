import flet as ft
from pathlib import Path
from core.converter import PowerPointConverter
import os
import webbrowser
import logging

# הגדרת הלוגר
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # הדפסה לטרמינל
        logging.FileHandler('app.log')  # שמירה לקובץ
    ]
)
logger = logging.getLogger(__name__)

class PowerPointToHtmlApp:
    def __init__(self):
        logger.info("מאתחל את האפליקציה")
        self.converter = PowerPointConverter()
        self.current_file = None
        self.output_dir = None
        self.last_output_file = None
        self.page = None

    def main(self, page: ft.Page):
        """הפונקציה הראשית של האפליקציה"""
        logger.info("מאתחל את הממשק הגרפי")
        try:
            # שמירת אובייקט הדף
            self.page = page
            
            # הגדרות בסיסיות לדף
            self.page.title = "PowerPoint to HTML Converter"
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.rtl = True
            self.page.padding = 20
            
            logger.debug("מגדיר את גודל החלון")
            # הגדרות חלון
            self.page.window.maximized = False
            self.page.window.minimized = False
            self.page.window.width = 800
            self.page.window.height = 600
            self.page.window.min_width = 600
            self.page.window.min_height = 400
            self.page.window.center()

            # הגדרת אירועי חלון
            def window_event_handler(e):
                logger.debug(f"אירוע חלון: {e.data}")
                if e.data == "resize":
                    # שמירה על גודל מינימלי
                    if self.page.window.width < 600:
                        self.page.window.width = 600
                    if self.page.window.height < 400:
                        self.page.window.height = 400
                    self.page.update()

            self.page.window.on_event = window_event_handler
            
            logger.debug("יוצר רכיבי ממשק")
            # יצירת רכיבי הממשק
            self.file_picker = ft.FilePicker(
                on_result=self.file_picker_result
            )
            self.page.overlay.append(self.file_picker)
            
            self.dir_picker = ft.FilePicker(
                on_result=self.dir_picker_result
            )
            self.page.overlay.append(self.dir_picker)
            
            # כפתור בחירת קובץ
            self.select_file_button = ft.ElevatedButton(
                "בחר מצגת PowerPoint",
                icon=ft.Icons.FILE_UPLOAD,
                on_click=lambda _: self.file_picker.pick_files(
                    allowed_extensions=["pptx"]
                )
            )
            
            # כפתור בחירת תיקיית פלט
            self.select_dir_button = ft.ElevatedButton(
                "בחר תיקיית פלט",
                icon=ft.Icons.FOLDER_OPEN,
                on_click=lambda _: self.dir_picker.get_directory_path()
            )
            
            # כפתור המרה
            self.convert_button = ft.ElevatedButton(
                "המר ל-HTML",
                icon=ft.Icons.TRANSFORM,
                on_click=self.convert_file,
                disabled=True
            )
            
            # כפתור תצוגה מקדימה
            self.preview_button = ft.ElevatedButton(
                "תצוגה מקדימה",
                icon=ft.Icons.PREVIEW,
                on_click=self.preview_html,
                disabled=True
            )
            
            # כפתור ייצוא לוג
            self.export_log_button = ft.ElevatedButton(
                "ייצא קובץ לוג",
                icon=ft.Icons.DESCRIPTION,
                on_click=self.export_error_log,
            )
            
            logger.debug("יוצר רכיבי טקסט")
            # טקסט נתיב הקובץ
            self.file_path_text = ft.Text(
                "לא נבחר קובץ",
                size=16,
                weight=ft.FontWeight.BOLD
            )
            
            # טקסט נתיב תיקיית הפלט
            self.output_dir_text = ft.Text(
                "לא נבחרה תיקייה",
                size=16,
                weight=ft.FontWeight.BOLD
            )
            
            # מיכל לטקסט תיקיית הפלט
            output_dir_container = ft.Container(
                content=self.output_dir_text,
                padding=10,
                border_radius=5,
                bgcolor="#E3F2FD"  # צבע רקע כחול בהיר
            )
            
            # כותרת ראשית
            title = ft.Text(
                "ממיר מצגות PowerPoint ל-HTML",
                size=32,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
            
            # כותרת משנה
            subtitle = ft.Text(
                "המר מצגות PowerPoint למסמכי HTML אינטראקטיביים",
                size=16,
                text_align=ft.TextAlign.CENTER
            )
            
            divider = ft.Divider(height=40)
            
            # טקסט סטטוס
            self.status_text = ft.Text(
                "",
                size=14,
                text_align=ft.TextAlign.CENTER,
                italic=True
            )
            
            logger.debug("יוצר את המיכל הראשי")
            # מיכל ראשי
            container = ft.Container(
                content=ft.Column(
                    controls=[
                        title,
                        subtitle,
                        divider,
                        self.file_path_text,
                        output_dir_container,
                        ft.Row(
                            controls=[
                                self.select_file_button,
                                self.select_dir_button,
                                self.convert_button,
                                self.preview_button,
                                self.export_log_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        self.status_text
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                border_radius=10,
                bgcolor="#FFFFFF"
            )
            
            logger.info("מוסיף את המיכל הראשי לדף")
            self.page.add(container)
            self.page.update()

        except Exception as e:
            logger.error(f"שגיאה באתחול הממשק: {str(e)}", exc_info=True)
            raise

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        try:
            if e.files:
                file_path = e.files[0].path
                logger.info(f"נבחר קובץ: {file_path}")
                self.current_file = file_path
                self.file_path_text.value = f"קובץ נבחר: {Path(file_path).name}"
                self.update_convert_button()
                self.status_text.value = ""
                self.preview_button.disabled = True
            else:
                logger.info("לא נבחר קובץ")
                self.current_file = None
                self.file_path_text.value = "לא נבחר קובץ"
                self.convert_button.disabled = True
            
            self.file_path_text.update()
            self.convert_button.update()
            self.preview_button.update()
        
        except Exception as e:
            logger.error(f"שגיאה בבחירת קובץ: {str(e)}", exc_info=True)

    def dir_picker_result(self, e: ft.FilePickerResultEvent):
        try:
            if e.path:
                logger.info(f"נבחרה תיקייה: {e.path}")
                self.output_dir = e.path
                self.output_dir_text.value = f"תיקיית פלט: {Path(e.path).name}"
                self.update_convert_button()
                self.status_text.value = ""
            else:
                logger.info("לא נבחרה תיקייה")
                self.output_dir = None
                self.output_dir_text.value = "לא נבחרה תיקייה"
                self.convert_button.disabled = True
            
            self.output_dir_text.update()
            self.convert_button.update()
        
        except Exception as e:
            logger.error(f"שגיאה בבחירת תיקייה: {str(e)}", exc_info=True)

    def update_convert_button(self):
        try:
            can_convert = bool(self.current_file and self.output_dir)
            logger.debug(f"עדכון כפתור המרה. מאופשר: {can_convert}")
            self.convert_button.disabled = not can_convert
            self.convert_button.update()
        
        except Exception as e:
            logger.error(f"שגיאה בעדכון כפתור המרה: {str(e)}", exc_info=True)

    def convert_file(self, e):
        """ממיר את קובץ ה-PowerPoint ל-HTML"""
        try:
            if not self.current_file or not os.path.exists(self.current_file):
                logger.error("לא נבחר קובץ PowerPoint להמרה")
                self.show_error_dialog("שגיאה", "אנא בחר קובץ PowerPoint להמרה")
                return

            if not self.output_dir or not os.path.exists(self.output_dir):
                logger.error("לא נבחרה תיקיית פלט")
                self.show_error_dialog("שגיאה", "אנא בחר תיקיית פלט")
                return

            # יצירת שם קובץ הפלט
            input_filename = os.path.splitext(os.path.basename(self.current_file))[0]
            output_filename = f"{input_filename}.html"
            output_path = os.path.join(self.output_dir, output_filename)

            # המרת המצגת
            logger.info(f"מתחיל המרה של {self.current_file} ל-{output_path}")
            self.converter.convert(self.current_file, output_path)
            
            # עדכון הנתיב האחרון
            self.last_output_file = output_path
            
            # הפעלת כפתור התצוגה המקדימה
            if hasattr(self, 'preview_button'):
                self.preview_button.disabled = False
                self.page.update()

            logger.info("ההמרה הושלמה בהצלחה")
            self.show_success_dialog("הצלחה", "המצגת הומרה בהצלחה ל-HTML")

        except Exception as ex:
            logger.error(f"שגיאה בהמרת הקובץ: {str(ex)}")
            self.show_error_dialog("שגיאה", f"שגיאה בהמרת הקובץ: {str(ex)}")

    def preview_html(self, e):
        """פותח את קובץ ה-HTML בדפדפן"""
        try:
            if self.last_output_file and os.path.exists(self.last_output_file):
                logger.info(f"פותח קובץ בדפדפן: {self.last_output_file}")
                # שימוש בנתיב מוחלט
                abs_path = os.path.abspath(self.last_output_file)
                # המרה לפורמט URL תקין
                file_url = f"file:///{abs_path.replace(os.sep, '/')}"
                # פתיחה בדפדפן ברירת המחדל
                webbrowser.open(file_url, new=2)
            else:
                logger.error("לא נמצא קובץ HTML לתצוגה מקדימה")
                self.show_error_dialog("שגיאה", "לא נמצא קובץ HTML לתצוגה מקדימה")
        except Exception as ex:
            logger.error(f"שגיאה בפתיחת הקובץ בדפדפן: {str(ex)}")
            self.show_error_dialog("שגיאה", f"שגיאה בפתיחת הקובץ בדפדפן: {str(ex)}")

    def export_error_log(self, e):
        """ייצוא קובץ הלוג"""
        try:
            save_path = ft.FilePicker(
                dialog_title="שמור קובץ לוג",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["log"],
                save_file=True,
            )
            
            def save_result(e):
                if e.path:
                    try:
                        with open('app.log', 'r', encoding='utf-8') as source:
                            with open(e.path, 'w', encoding='utf-8') as target:
                                target.write(source.read())
                        self.show_message("הצלחה", "קובץ הלוג נשמר בהצלחה")
                    except Exception as ex:
                        logger.error(f"שגיאה בשמירת קובץ הלוג: {str(ex)}")
                        self.show_message("שגיאה", f"שגיאה בשמירת קובץ הלוג: {str(ex)}")
            
            save_path.on_result = save_result
            self.page.overlay.append(save_path)
            save_path.save_file()
            self.page.update()
        except Exception as ex:
            logger.error(f"שגיאה בייצוא הלוג: {str(ex)}")
            self.show_message("שגיאה", f"שגיאה בייצוא הלוג: {str(ex)}")

    def show_error_dialog(self, title, message):
        """מציג דיאלוג שגיאה"""
        try:
            if not self.page:
                logger.error("אין אובייקט page זמין")
                return
                
            def close_dialog(e):
                if self.error_dialog:
                    self.error_dialog.open = False
                    self.page.update()

            self.error_dialog = ft.AlertDialog(
                title=ft.Text(title),
                content=ft.Text(message),
                actions=[
                    ft.ElevatedButton("סגור", on_click=close_dialog)
                ]
            )
            self.page.overlay.append(self.error_dialog)
            self.error_dialog.open = True
            self.page.update()
            
        except Exception as ex:
            logger.error(f"שגיאה בהצגת דיאלוג שגיאה: {str(ex)}")

    def show_success_dialog(self, title, message):
        """מציג דיאלוג הצלחה"""
        try:
            if not self.page:
                logger.error("אין אובייקט page זמין")
                return
                
            def close_dialog(e):
                if self.success_dialog:
                    self.success_dialog.open = False
                    self.page.update()

            self.success_dialog = ft.AlertDialog(
                title=ft.Text(title),
                content=ft.Text(message),
                actions=[
                    ft.ElevatedButton("סגור", on_click=close_dialog)
                ]
            )
            self.page.overlay.append(self.success_dialog)
            self.success_dialog.open = True
            self.page.update()
            
        except Exception as ex:
            logger.error(f"שגיאה בהצגת דיאלוג הצלחה: {str(ex)}")

    def show_message(self, title, message):
        """מציג הודעה"""
        try:
            if not self.page:
                logger.error("אין אובייקט page זמין")
                return
                
            def close_dialog(e):
                if self.message_dialog:
                    self.message_dialog.open = False
                    self.page.update()

            self.message_dialog = ft.AlertDialog(
                title=ft.Text(title),
                content=ft.Text(message),
                actions=[
                    ft.ElevatedButton("סגור", on_click=close_dialog)
                ]
            )
            self.page.overlay.append(self.message_dialog)
            self.message_dialog.open = True
            self.page.update()
            
        except Exception as ex:
            logger.error(f"שגיאה בהצגת הודעה: {str(ex)}")

def main():
    logger.info("מתחיל את האפליקציה")
    try:
        app = PowerPointToHtmlApp()
        ft.app(target=app.main)
    except Exception as e:
        logger.error(f"שגיאה בהרצת האפליקציה: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
