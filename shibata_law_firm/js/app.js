// Dynamic Star Background Generation
function generateStars() {
    const container = document.getElementById('stars-container');
    const numStars = 100;
    
    for (let i = 0; i < numStars; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        
        // Random positions
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        
        // Random sizes, favoring smaller stars
        const size = Math.random() < 0.8 ? (Math.random() * 2) : (Math.random() * 3 + 1);
        
        // Random blink duration
        const duration = Math.random() * 3 + 2;
        const delay = Math.random() * 5;
        
        star.style.left = `${x}vw`;
        star.style.top = `${y}vh`;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.animationDuration = `${duration}s`;
        star.style.animationDelay = `${delay}s`;
        
        container.appendChild(star);
    }
}

// Scroll interactions using Intersection Observer
function initScrollObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: stop observing once faded in
                // observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15
    });

    document.querySelectorAll('.fade-in-scroll').forEach(element => {
        observer.observe(element);
    });
}

// Form Submission prevention (Demo only)
function initForm() {
    const form = document.querySelector('.contact-form');
    if(form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const originalText = btn.innerText;
            btn.innerText = "Message Transmitted 🚀";
            btn.style.background = "#4CAF50";
            
            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.background = "";
                form.reset();
            }, 3000);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    generateStars();
    initScrollObserver();
    initForm();
});
