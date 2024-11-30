from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QFileDialog, QProgressBar, QLabel, QTextEdit)
from PyQt6.QtCore import Qt
from core.converter import PowerPointConverter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PowerPoint to HTML Converter")
        self.setMinimumSize(600, 400)
        
        # מרכיבי הממשק
        self.setup_ui()
        
        # אתחול הממיר
        self.converter = PowerPointConverter()
        
    def setup_ui(self):
        # יצירת ווידג'ט מרכזי
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # יצירת layout ראשי
        layout = QVBoxLayout(central_widget)
        
        # כפתור בחירת קובץ
        self.select_file_btn = QPushButton("בחר קובץ PowerPoint")
        self.select_file_btn.clicked.connect(self.select_file)
        
        # תווית להצגת שם הקובץ הנבחר
        self.file_label = QLabel("לא נבחר קובץ")
        
        # סרגל התקדמות
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # כפתור המרה
        self.convert_btn = QPushButton("המר ל-HTML")
        self.convert_btn.clicked.connect(self.convert_file)
        self.convert_btn.setEnabled(False)
        
        # כפתור ייצוא קוד הטמעה
        self.embed_btn = QPushButton("ייצא קוד להטמעה ב-Wix")
        self.embed_btn.clicked.connect(self.generate_embed_code)
        self.embed_btn.setEnabled(False)
        
        # אזור הצגת קוד הטמעה
        self.embed_code_area = QTextEdit()
        self.embed_code_area.setReadOnly(True)
        
        # הוספת הרכיבים ל-layout
        layout.addWidget(self.select_file_btn)
        layout.addWidget(self.file_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.embed_btn)
        layout.addWidget(self.embed_code_area)
        layout.addStretch()
        
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "בחר קובץ PowerPoint",
            "",
            "PowerPoint Files (*.pptx *.ppt)"
        )
        
        if file_name:
            self.file_label.setText(file_name)
            self.convert_btn.setEnabled(True)
            
    def convert_file(self):
        if not self.file_label.text() or self.file_label.text() == "לא נבחר קובץ":
            return
            
        self.progress_bar.setVisible(True)
        self.convert_btn.setEnabled(False)
        
        # כאן נוסיף את הלוגיקה של ההמרה
        try:
            output_path = self.converter.convert(self.file_label.text())
            self.show_success_message(output_path)
            self.embed_btn.setEnabled(True)
        except Exception as e:
            self.show_error_message(str(e))
        finally:
            self.progress_bar.setVisible(False)
            self.convert_btn.setEnabled(True)
            
    def generate_embed_code(self):
        if not self.file_label.text() or self.file_label.text() == "לא נבחר קובץ":
            return
            
        try:
            # יצירת קוד ההטמעה
            embed_code_path, embed_path = self.converter.generate_embed_code(
                self.file_label.text(),
                width="100%",
                height="600px",
                responsive=True
            )
            
            # הצגת קוד ההטמעה
            with open(embed_code_path, 'r') as file:
                embed_code = file.read()
                self.embed_code_area.setText(embed_code)
                
            # הצגת הודעת הצלחה עם הוראות
            self.show_success_message("קוד ההטמעה נוצר בהצלחה!\n"
                                      "1. העלה את הקובץ " + os.path.basename(embed_path) + " לשרת\n"
                                      "2. העתק את קוד ההטמעה מהקובץ " + os.path.basename(embed_code_path) + "\n"
                                      "3. הדבק את הקוד באתר Wix שלך")
            
        except Exception as ex:
            self.show_error_message("שגיאה ביצירת קוד הטמעה: " + str(ex))
            
    def show_success_message(self, message):
        # נוסיף בהמשך
        print(message)
        
    def show_error_message(self, error):
        # נוסיף בהמשך
        print(error)
