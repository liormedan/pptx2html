from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QFileDialog, QProgressBar, QLabel)
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
        
        # הוספת הרכיבים ל-layout
        layout.addWidget(self.select_file_btn)
        layout.addWidget(self.file_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.convert_btn)
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
        except Exception as e:
            self.show_error_message(str(e))
        finally:
            self.progress_bar.setVisible(False)
            self.convert_btn.setEnabled(True)
            
    def show_success_message(self, output_path):
        # נוסיף בהמשך
        pass
        
    def show_error_message(self, error):
        # נוסיף בהמשך
        pass
