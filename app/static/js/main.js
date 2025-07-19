/**
 * Main JavaScript file for the Police Case Management System
 */

// Document ready function
$(document).ready(function() {
    // Initialize tooltips
    initTooltips();
    
    // Auto-hide alerts after 5 seconds
    autoHideAlerts();
    
    // Add animation classes to elements that need animation on scroll
    animateOnScroll();
    
    // Initialize dark mode toggle if present
    initDarkModeToggle();
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-hide alerts after timeout
 */
function autoHideAlerts() {
    setTimeout(function() {
        $(".alert").alert('close');
    }, 5000);
}

/**
 * Add animation classes to elements on scroll
 */
function animateOnScroll() {
    // Check if IntersectionObserver is supported
    if ('IntersectionObserver' in window) {
        const animateElements = document.querySelectorAll('.animate-on-scroll');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', entry.target.dataset.animation || 'animate__fadeIn');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        animateElements.forEach(element => {
            observer.observe(element);
        });
    }
}

/**
 * Initialize dark mode toggle
 */
function initDarkModeToggle() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (darkModeToggle) {
        // Check if user has dark mode preference
        const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        
        // Apply dark mode if saved or preferred
        if (savedDarkMode || prefersDarkMode) {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }
        
        // Toggle dark mode on change
        darkModeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'true');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'false');
            }
        });
    }
}

/**
 * Format timestamps to readable format
 * @param {string} timestamp - ISO timestamp
 * @returns {string} - Formatted time
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

/**
 * Show loading spinner
 * @param {string} elementId - ID of element to show spinner in
 * @param {string} text - Loading text
 */
function showSpinner(elementId, text = 'Loading...') {
    const element = document.getElementById(elementId);
    
    if (element) {
        element.innerHTML = `
            <div class="d-flex justify-content-center align-items-center">
                <div class="spinner-border text-primary me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span>${text}</span>
            </div>
        `;
    }
}

/**
 * Hide loading spinner
 * @param {string} elementId - ID of element to hide spinner from
 */
function hideSpinner(elementId) {
    const element = document.getElementById(elementId);
    
    if (element) {
        element.innerHTML = '';
    }
}
