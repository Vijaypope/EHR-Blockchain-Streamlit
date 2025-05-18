def add_page_animations():
    """Add animations and visual effects to the Streamlit app"""
    
    # Add animation and interactivity with JavaScript
    animation_js = """
    <script>
        // Function to add animation classes to elements when they become visible
        function animateOnScroll() {
            const elements = document.querySelectorAll('.stApp div div');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.transition = 'all 0.5s ease-out';
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });
            
            // Apply initial styles and observe elements
            elements.forEach(element => {
                // Skip elements that already have animation classes
                if (element.classList.contains('fadeIn') || 
                    element.classList.contains('slideIn') ||
                    element.classList.contains('auth-container') ||
                    element.classList.contains('blockchain-container')) {
                    return;
                }
                
                // Apply initial styles
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                observer.observe(element);
            });
        }
        
        // Run on load and when content changes
        document.addEventListener('DOMContentLoaded', animateOnScroll);
        
        // Create a MutationObserver to detect DOM changes
        const observer = new MutationObserver(animateOnScroll);
        
        // Start observing changes to the DOM
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Add hover animations to buttons
        function addButtonAnimations() {
            const buttons = document.querySelectorAll('button');
            
            buttons.forEach(button => {
                button.addEventListener('mouseenter', () => {
                    button.style.transform = 'translateY(-2px)';
                    button.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
                });
                
                button.addEventListener('mouseleave', () => {
                    button.style.transform = 'translateY(0)';
                    button.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                });
            });
        }
        
        // Run button animations
        setInterval(addButtonAnimations, 1000);
    </script>
    """
    
    # Add the JavaScript to the Streamlit app
    from streamlit import components
    components.v1.html(animation_js, height=0
