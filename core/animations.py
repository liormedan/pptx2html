class AnimationHandler:
    """מנהל האנימציות של המצגת"""
    
    ANIMATION_EFFECTS = {
        'FADE': 'fade',
        'SLIDE_LEFT': 'slide-left',
        'SLIDE_RIGHT': 'slide-right',
        'SLIDE_UP': 'slide-up',
        'SLIDE_DOWN': 'slide-down',
        'ZOOM_IN': 'zoom-in',
        'ZOOM_OUT': 'zoom-out',
        'ROTATE': 'rotate'
    }

    def get_animation_css(self):
        """מחזיר את הגדרות ה-CSS לאנימציות"""
        return """
            @keyframes fade {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slide-left {
                from { transform: translateX(-100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes slide-right {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes slide-up {
                from { transform: translateY(100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes slide-down {
                from { transform: translateY(-100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes zoom-in {
                from { transform: scale(0); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            
            @keyframes zoom-out {
                from { transform: scale(2); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            
            @keyframes rotate {
                from { transform: rotate(-180deg); opacity: 0; }
                to { transform: rotate(0); opacity: 1; }
            }
            
            .animated {
                animation-duration: 1s;
                animation-fill-mode: both;
            }
            
            .fade { animation-name: fade; }
            .slide-left { animation-name: slide-left; }
            .slide-right { animation-name: slide-right; }
            .slide-up { animation-name: slide-up; }
            .slide-down { animation-name: slide-down; }
            .zoom-in { animation-name: zoom-in; }
            .zoom-out { animation-name: zoom-out; }
            .rotate { animation-name: rotate; }
        """

    def get_animation_script(self):
        """מחזיר את קוד ה-JavaScript לניהול האנימציות"""
        return """
            const animationController = {
                animations: {},
                currentSlide: 0,
                currentStep: 0,
                
                addAnimation: function(elementId, effect, timing) {
                    const slideId = parseInt(elementId.split('-')[1]);
                    if (!this.animations[slideId]) {
                        this.animations[slideId] = [];
                    }
                    
                    this.animations[slideId].push({
                        elementId: elementId,
                        effect: effect,
                        step: timing.step || 0,
                        delay: timing.delay || 0,
                        duration: timing.duration || 1
                    });
                },
                
                playStep: function() {
                    const slideAnimations = this.animations[this.currentSlide] || [];
                    const currentStepAnimations = slideAnimations.filter(
                        anim => anim.step === this.currentStep
                    );
                    
                    if (currentStepAnimations.length === 0) {
                        return false;
                    }
                    
                    currentStepAnimations.forEach(animation => {
                        const element = document.getElementById(animation.elementId);
                        if (element) {
                            element.style.visibility = 'visible';
                            element.classList.add('animated', animation.effect);
                            element.style.animationDelay = `${animation.delay}s`;
                            element.style.animationDuration = `${animation.duration}s`;
                        }
                    });
                    
                    this.currentStep++;
                    return true;
                },
                
                resetSlide: function() {
                    const elements = document.querySelectorAll('.animated');
                    elements.forEach(element => {
                        element.style.visibility = 'hidden';
                        element.classList.remove('animated');
                        element.classList.remove(...Object.values(animationController.EFFECTS));
                    });
                    this.currentStep = 0;
                },
                
                nextSlide: function() {
                    const slides = document.querySelectorAll('.slide');
                    if (this.currentSlide < slides.length - 1) {
                        slides[this.currentSlide].style.display = 'none';
                        this.currentSlide++;
                        slides[this.currentSlide].style.display = 'block';
                        this.resetSlide();
                    }
                },
                
                prevSlide: function() {
                    if (this.currentSlide > 0) {
                        const slides = document.querySelectorAll('.slide');
                        slides[this.currentSlide].style.display = 'none';
                        this.currentSlide--;
                        slides[this.currentSlide].style.display = 'block';
                        this.resetSlide();
                    }
                },
                
                EFFECTS: {
                    FADE: 'fade',
                    SLIDE_LEFT: 'slide-left',
                    SLIDE_RIGHT: 'slide-right',
                    SLIDE_UP: 'slide-up',
                    SLIDE_DOWN: 'slide-down',
                    ZOOM_IN: 'zoom-in',
                    ZOOM_OUT: 'zoom-out',
                    ROTATE: 'rotate'
                }
            };
            
            // מאזיני אירועים
            document.addEventListener('DOMContentLoaded', function() {
                // הסתרת כל השקופיות חוץ מהראשונה
                const slides = document.querySelectorAll('.slide');
                slides.forEach((slide, index) => {
                    slide.style.display = index === 0 ? 'block' : 'none';
                });
                
                // הסתרת כל האלמנטים המונפשים
                document.querySelectorAll('.animated').forEach(element => {
                    element.style.visibility = 'hidden';
                });
            });
            
            // מעבר בין שקופיות עם מקשי מקלדת
            document.addEventListener('keydown', function(event) {
                switch(event.key) {
                    case 'ArrowRight':
                    case 'PageDown':
                        if (!animationController.playStep()) {
                            animationController.nextSlide();
                        }
                        break;
                    case 'ArrowLeft':
                    case 'PageUp':
                        animationController.prevSlide();
                        break;
                    case ' ':
                        event.preventDefault();
                        if (!animationController.playStep()) {
                            animationController.nextSlide();
                        }
                        break;
                }
            });
            
            // תמיכה במגע
            let touchStartX = 0;
            document.addEventListener('touchstart', function(event) {
                touchStartX = event.touches[0].clientX;
            });
            
            document.addEventListener('touchend', function(event) {
                const touchEndX = event.changedTouches[0].clientX;
                const diff = touchStartX - touchEndX;
                
                if (Math.abs(diff) > 50) {  // מינימום מרחק להחלקה
                    if (diff > 0) {
                        if (!animationController.playStep()) {
                            animationController.nextSlide();
                        }
                    } else {
                        animationController.prevSlide();
                    }
                }
            });
        """

    def create_animation(self, effect_type='FADE', step=0, delay=0, duration=1):
        """יוצר אנימציה חדשה"""
        effect = self.ANIMATION_EFFECTS.get(effect_type, 'fade')
        return {
            'effect': effect,
            'step': step,
            'delay': delay,
            'duration': duration
        }

    def get_animation_style(self, animation):
        """מחזיר את הסגנון CSS לאנימציה"""
        if not animation:
            return ''
            
        return f"""
            visibility: hidden;
            animation-delay: {animation.get('delay', 0)}s;
            animation-duration: {animation.get('duration', 1)}s;
        """
