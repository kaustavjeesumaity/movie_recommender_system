// Initialize when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality elements
    const searchInput = document.getElementById('movie-search');
    const dropdown = document.getElementById('suggestions-dropdown');
    const suggestionItems = document.querySelectorAll('.suggestion-item');
    
    // Image error handling setup
    const moviePosters = document.querySelectorAll('.movie-poster-img');
    
    // Initialize search suggestions dropdown
    function initSearchSuggestions() {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            let hasMatches = false;
            
            // Filter and display matching suggestions
            suggestionItems.forEach(item => {
                const movieName = item.getAttribute('data-value').toLowerCase();
                if (movieName.includes(searchTerm)) {
                    item.style.display = 'block';
                    hasMatches = true;
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Show/hide dropdown based on matches
            dropdown.style.display = searchTerm && hasMatches ? 'block' : 'none';
        });
        
        // Handle suggestion selection
        suggestionItems.forEach(item => {
            item.addEventListener('click', function() {
                searchInput.value = this.getAttribute('data-value');
                dropdown.style.display = 'none';
            });
        });
        
        // Hide dropdown when clicking elsewhere
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    }

    // Initialize image error handling
    function initImageFallbacks() {
        moviePosters.forEach(img => {
            // Set up error handler
            img.addEventListener('error', handleImageError);
            
            // Check if image needs fallback immediately
            if (!img.src || img.complete && img.naturalHeight === 0) {
                handleImageError({ target: img });
            }
        });
    }

    // Handle image loading errors
    function handleImageError(e) {
        const img = e.target;
        img.onerror = null; // Prevent infinite loop
        
        // Use fallback image if available
        if (img.dataset.fallback) {
            img.src = img.dataset.fallback;
        }
        
        // Add broken image styling
        img.classList.add('broken-image');
    }

    // Initialize all functionality
    initSearchSuggestions();
    initImageFallbacks();

    // Optional: Add keyboard navigation for accessibility
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown' && dropdown.style.display === 'block') {
            const firstSuggestion = dropdown.querySelector('.suggestion-item[style="display: block;"]');
            if (firstSuggestion) firstSuggestion.focus();
        }
    });

    dropdown.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault();
            const current = document.activeElement;
            const suggestions = Array.from(dropdown.querySelectorAll('.suggestion-item[style="display: block;"]'));
            const currentIndex = suggestions.indexOf(current);
            
            if (e.key === 'ArrowDown' && currentIndex < suggestions.length - 1) {
                suggestions[currentIndex + 1].focus();
            } else if (e.key === 'ArrowUp' && currentIndex > 0) {
                suggestions[currentIndex - 1].focus();
            } else if (e.key === 'ArrowUp' && currentIndex === 0) {
                searchInput.focus();
            }
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (document.activeElement.classList.contains('suggestion-item')) {
                searchInput.value = document.activeElement.getAttribute('data-value');
                dropdown.style.display = 'none';
            }
        }
    });
});