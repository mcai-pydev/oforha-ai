// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Show/hide home button based on scroll position
    const homeButton = document.getElementById('go-home');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            homeButton.style.display = 'flex';
        } else {
            homeButton.style.display = 'none';
        }
    });

    // Handle recommendation form submission
    const recommendationForm = document.getElementById('recommendation-form');
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const position = document.getElementById('position').value;
            const message = document.getElementById('message').value;

            // Create new recommendation card
            const newRecommendation = document.createElement('div');
            newRecommendation.className = 'recommendation-card';
            newRecommendation.innerHTML = `
                <img src="https://via.placeholder.com/100" alt="${name}">
                <div class="recommendation-content">
                    <h3>${name}</h3>
                    <p>${position}</p>
                    <p>"${message}"</p>
                </div>
            `;

            // Add confirmation dialog
            if (confirm('Are you sure you want to submit this recommendation?')) {
                // Add new recommendation to the container
                const recommendationsContainer = document.querySelector('.recommendations-container');
                recommendationsContainer.appendChild(newRecommendation);

                // Reset form
                recommendationForm.reset();

                // Scroll to the new recommendation
                newRecommendation.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }

    // Add animation to skill cards on scroll
    const skillCards = document.querySelectorAll('.skill-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    skillCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease-out';
        observer.observe(card);
    });

    // Add animation to project cards on scroll
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease-out';
        observer.observe(card);
    });

    // Add animation to recommendation cards on scroll
    const recommendationCards = document.querySelectorAll('.recommendation-card');
    recommendationCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease-out';
        observer.observe(card);
    });
}); 