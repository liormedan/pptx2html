class StyleGenerator:
    @staticmethod
    def get_base_css():
        """מחזיר את הסגנונות הבסיסיים של המצגת"""
        return """
            :root {
                --base-font-size: 1em;
                --primary-color: #2196F3;
                --text-color: #333;
                --bg-color: #fff;
                --nav-bg: rgba(255, 255, 255, 0.9);
                --thumbnail-bg: #f5f5f5;
                --thumbnail-active: #e0e0e0;
                --settings-bg: rgba(255, 255, 255, 0.95);
                --settings-border: #ddd;
                --button-hover: #1976D2;
                --container-width: 1024px;  /* רוחב סטנדרטי */
                --slide-width: 800px;
                --frame-bg: #f8f9fa;
                --menu-z-index: 1000;
                --content-z-index: 1;
            }
            
            [data-theme="dark"] {
                --text-color: #fff;
                --bg-color: #1a1a1a;
                --nav-bg: rgba(26, 26, 26, 0.9);
                --thumbnail-bg: #2d2d2d;
                --thumbnail-active: #404040;
                --settings-bg: rgba(26, 26, 26, 0.95);
                --settings-border: #404040;
                --button-hover: #1565C0;
                --frame-bg: #2d2d2d;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: system-ui, -apple-system, sans-serif;
                font-size: var(--base-font-size);
                line-height: 1.6;
                color: var(--text-color);
                background: var(--bg-color);
                transition: background-color 0.3s, color 0.3s;
                direction: rtl;
                min-height: 100vh;
                padding: 20px;
            }
            
            .main-container {
                max-width: var(--container-width);
                margin: 0 auto;
                background: var(--frame-bg);
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                min-height: calc(100vh - 40px);
                display: flex;
                position: relative;
            }
            
            .content-area {
                flex: 1;
                padding: 20px;
                padding-right: 240px; /* מרווח לתפריט */
                overflow-x: hidden;
            }
            
            .presentation {
                background: var(--bg-color);
                border-radius: 8px;
                padding: 40px;
                width: 100%;
                max-width: var(--slide-width);
                margin: 0 auto;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            .slide {
                display: none;
                background: var(--bg-color);
                border-radius: 8px;
                margin-bottom: 20px;
                width: 100%;
                aspect-ratio: 16/9;
                overflow: hidden;
            }
            
            .slide.active {
                display: block;
            }
            
            .slide-content {
                height: 100%;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }
            
            .slide img {
                max-width: 100%;
                height: auto;
                border-radius: 4px;
                margin: 10px 0;
            }
            
            .nav-buttons {
                position: fixed;
                bottom: 40px;
                right: 50%;
                transform: translateX(50%);
                display: flex;
                gap: 10px;
                background: var(--nav-bg);
                padding: 10px 20px;
                border-radius: 50px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                z-index: 100;
            }
            
            .nav-button {
                background: var(--primary-color);
                color: white;
                border: none;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
                transition: background-color 0.3s;
            }
            
            .nav-button:hover {
                background: var(--button-hover);
            }
            
            .slide-indicator {
                position: fixed;
                top: 40px;
                right: 50%;
                transform: translateX(50%);
                background: var(--nav-bg);
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                z-index: 100;
            }
            
            .thumbnails-container {
                position: absolute;
                right: 0;
                top: 0;
                bottom: 0;
                width: 220px;
                background: var(--thumbnail-bg);
                padding: 20px 10px;
                overflow-y: auto;
                border-radius: 0 12px 12px 0;
                border-right: 1px solid var(--settings-border);
            }
            
            .thumbnail {
                background: var(--bg-color);
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 10px;
                cursor: pointer;
                transition: background-color 0.3s;
                position: relative;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .thumbnail:hover {
                background: var(--thumbnail-active);
            }
            
            .thumbnail.active {
                background: var(--thumbnail-active);
                border-right: 3px solid var(--primary-color);
            }
            
            .thumb-number {
                font-size: 12px;
                color: var(--text-color);
                text-align: center;
            }
            
            .settings-button {
                position: fixed;
                top: 40px;
                left: 40px;
                background: var(--nav-bg);
                border: none;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                z-index: 110;
            }
            
            .settings-panel {
                position: fixed;
                top: 90px;
                left: 40px;
                background: var(--settings-bg);
                border: 1px solid var(--settings-border);
                border-radius: 8px;
                padding: 15px;
                width: 250px;
                display: none;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                z-index: 110;
            }
            
            .settings-panel.active {
                display: block;
            }
            
            .settings-panel div {
                margin-bottom: 10px;
            }
            
            .settings-panel label {
                display: block;
                margin-bottom: 5px;
            }
            
            .settings-panel select {
                width: 100%;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid var(--settings-border);
                background: var(--bg-color);
                color: var(--text-color);
            }
            
            .settings-divider {
                border-top: 1px solid var(--settings-border);
                margin: 15px 0;
            }
            
            .export-button {
                width: 100%;
                padding: 10px;
                background: var(--primary-color);
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.3s;
            }
            
            .export-button:hover {
                background: var(--button-hover);
            }
            
            /* סגנונות התפריט */
            .menu-container {
                position: fixed;
                top: 0;
                right: 0;
                width: 250px;
                height: 100vh;
                background: var(--nav-bg);
                border-left: 1px solid var(--settings-border);
                padding: 20px;
                overflow-y: auto;
                z-index: var(--menu-z-index);
                box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
            }

            /* אזור התוכן הראשי */
            .main-content {
                margin-right: 250px;
                padding: 20px;
                z-index: var(--content-z-index);
                position: relative;
            }

            /* מיכל המצגת */
            .presentation-container {
                max-width: var(--container-width);
                margin: 0 auto;
                background: var(--frame-bg);
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }

            /* התמונה המוצגת */
            .slide-image {
                width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
                max-width: var(--slide-width);
                border-radius: 4px;
            }
            
            @media (max-width: 1200px) {
                .main-container {
                    max-width: 100%;
                }
            }
            
            @media (max-width: 768px) {
                .content-area {
                    padding: 20px;
                }
                
                .thumbnails-container {
                    display: none;
                }
                
                .settings-panel {
                    width: calc(100% - 80px);
                }
                
                .presentation {
                    padding: 20px;
                }
            }
        """

    @staticmethod
    def get_presentation_script():
        """מחזיר את קוד ה-JavaScript הבסיסי לניווט במצגת"""
        return """
            let currentSlide = 0;
            const slides = document.querySelectorAll('.slide');
            
            function showSlide(index, direction = 'next') {
                if (index < 0) index = slides.length - 1;
                if (index >= slides.length) index = 0;
                
                // הסתרת השקופית הנוכחית
                if (slides[currentSlide]) {
                    slides[currentSlide].classList.remove('active');
                }
                
                // הצגת השקופית החדשה
                slides[index].classList.add('active');
                currentSlide = index;
                
                // הפעלת אנימציות בשקופית החדשה
                if (window.animationController) {
                    window.animationController.resetAnimations();
                    window.animationController.playSlideAnimations(currentSlide);
                }
            }
            
            function nextSlide() {
                showSlide(currentSlide + 1, 'next');
            }
            
            function prevSlide() {
                showSlide(currentSlide - 1, 'prev');
            }
            
            // מקשי מקלדת
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight' || e.key === 'PageUp') {
                    prevSlide();
                } else if (e.key === 'ArrowLeft' || e.key === 'PageDown') {
                    nextSlide();
                }
            });
            
            // הצגת השקופית הראשונה
            window.addEventListener('load', () => {
                showSlide(0);
            });
        """
