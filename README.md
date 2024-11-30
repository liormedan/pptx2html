# PowerPoint to HTML Converter

ממיר מצגות PowerPoint לדפי HTML אינטראקטיביים עם תמיכה מלאה בעברית.

## תכונות עיקריות

- המרת מצגות PowerPoint לדפי HTML מותאמים
- תמיכה מלאה בעברית (RTL)
- ממשק משתמש נוח ואינטואיטיבי
- תצוגת תמונות ממוזערות לניווט מהיר
- מצב כהה/בהיר
- התאמת גודל טקסט
- תמיכה בניווט באמצעות מקלדת
- שמירת העדפות משתמש

## דרישות מערכת

- Python 3.8 ומעלה
- הספריות הנדרשות מפורטות בקובץ requirements.txt

## התקנה

1. שכפל את הרפוזיטורי:
```bash
git clone https://github.com/YOUR_USERNAME/pptx2html.git
cd pptx2html
```

2. צור והפעל סביבה וירטואלית:
```bash
python -m venv env
env\Scripts\activate  # Windows
```

3. התקן את הספריות הנדרשות:
```bash
pip install -r requirements.txt
```

## שימוש

הרץ את התוכנית:
```bash
python main.py
```

1. לחץ על "בחר מצגת PowerPoint" לבחירת קובץ המצגת
2. בחר תיקיית יעד לשמירת קובץ ה-HTML
3. לחץ על "המר ל-HTML" להמרת המצגת

## תכונות נוספות

- ניווט בין שקופיות באמצעות כפתורים או מקשי חצים
- שינוי ערכת נושא (בהיר/כהה)
- התאמת גודל טקסט
- תצוגה מקדימה של שקופיות
- ייצוא קובץ לוג לצורך פתרון בעיות

## רישיון

MIT License - ראה קובץ [LICENSE](LICENSE) לפרטים נוספים.