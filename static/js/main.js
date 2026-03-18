// JavaScript for Navigation and Interactions

document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    const currentLocation = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // Smooth scrolling for internal links
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Dynamic content loading example
    async function loadPortfolios() {
        try {
            const response = await fetch('/api/portfolios');
            const data = await response.json();
            console.log(data);
            // Render data to the page
        } catch (error) {
            console.error('Error loading portfolios:', error);
        }
    }

    loadPortfolios();
});