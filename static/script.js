// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    console.log('App initialized');
    checkSession();
    loadMovies();
    loadMyRecommendations();
    loadMoviesToRate();
    loadMyRatings();
});

// Check session
async function checkSession() {
    try {
        const response = await fetch('/api/debug/session');
        const data = await response.json();
        console.log('Session info:', data);
        
        if (!data.has_user_id) {
            console.warn('⚠️ User not logged in!');
            showToast('Please log in to rate movies', 'error');
        } else {
            console.log('✅ User logged in:', data.username);
        }
    } catch (error) {
        console.error('Error checking session:', error);
    }
}

// Tab switching
function showTab(tabName) {
    console.log('Switching to tab:', tabName);
    
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Load data for specific tabs
    if (tabName === 'my-recommendations') {
        loadMyRecommendations();
    } else if (tabName === 'rate-movies') {
        loadMoviesToRate();
    } else if (tabName === 'ratings') {
        loadMyRatings();
    }
}

// Load movies
let allMovies = [];
async function loadMovies() {
    try {
        const response = await fetch('/api/movies');
        allMovies = await response.json();
        console.log('Movies loaded:', allMovies.length);
        
        const select = document.getElementById('content-movie');
        if (select) {
            select.innerHTML = '<option value="">Choose a movie...</option>';
            allMovies.forEach(movie => {
                const option = document.createElement('option');
                option.value = movie.movie_id;
                option.textContent = `${movie.title} (${movie.genres})`;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading movies:', error);
    }
}

// Load my recommendations
async function loadMyRecommendations() {
    const count = document.getElementById('my-rec-count')?.value || 8;
    const resultsDiv = document.getElementById('my-rec-results');
    
    if (!resultsDiv) return;
    
    resultsDiv.innerHTML = '<div class="loading">🎬 Loading your recommendations...</div>';
    
    try {
        const response = await fetch(`/api/recommend/my_recommendations?n=${count}`);
        const recommendations = await response.json();
        
        if (recommendations.error) {
            resultsDiv.innerHTML = `<div class="info-message">
                <h3>👋 Welcome!</h3>
                <p>${recommendations.error}</p>
                <p>Go to the "Rate Movies" tab to start rating movies and get personalized recommendations!</p>
            </div>`;
            return;
        }
        
        displayRecommendations(recommendations, resultsDiv);
    } catch (error) {
        console.error('Error loading recommendations:', error);
        resultsDiv.innerHTML = '<div class="error">Error loading recommendations</div>';
    }
}

// Load movies to rate
async function loadMoviesToRate() {
    const container = document.getElementById('movies-to-rate');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Loading movies...</div>';
    
    try {
        const moviesResponse = await fetch('/api/movies');
        console.log('Movies response status:', moviesResponse.status);
        
        if (!moviesResponse.ok) {
            const errorData = await moviesResponse.json();
            console.error('Movies API error:', errorData);
            container.innerHTML = `<div class="error">Error: ${errorData.error || 'Failed to load movies'}</div>`;
            return;
        }
        
        const movies = await moviesResponse.json();
        console.log('Movies loaded:', movies);
        
        if (!Array.isArray(movies) || movies.length === 0) {
            container.innerHTML = '<div class="error">No movies available</div>';
            return;
        }
        
        const ratingsResponse = await fetch('/api/my_ratings');
        console.log('Ratings response status:', ratingsResponse.status);
        
        let myRatings = [];
        if (ratingsResponse.ok) {
            myRatings = await ratingsResponse.json();
            console.log('My ratings:', myRatings);
        }
        
        // Create a map of existing ratings
        const ratingsMap = {};
        if (Array.isArray(myRatings)) {
            myRatings.forEach(rating => {
                const movie = movies.find(m => m.title === rating.title);
                if (movie) {
                    ratingsMap[movie.movie_id] = rating.rating;
                }
            });
        }
        
        console.log('Ratings map:', ratingsMap);
        
        container.innerHTML = movies.map(movie => {
            const currentRating = ratingsMap[movie.movie_id] || 0;
            return `
                <div class="rate-movie-card" data-movie-id="${movie.movie_id}">
                    <h3>${movie.title}</h3>
                    <div class="movie-genres">
                        ${movie.genres.split('|').map(genre => 
                            `<span class="genre-tag">${genre}</span>`
                        ).join('')}
                    </div>
                    <div class="rating-stars" data-movie-id="${movie.movie_id}">
                        ${[1, 2, 3, 4, 5].map(star => `
                            <span class="star ${currentRating >= star ? 'filled' : ''}" 
                                  data-rating="${star}"
                                  onclick="rateMovie(${movie.movie_id}, ${star})">
                                ⭐
                            </span>
                        `).join('')}
                    </div>
                    <div class="current-rating" id="rating-text-${movie.movie_id}">
                        ${currentRating ? `Your rating: ${currentRating}/5` : 'Click stars to rate'}
                    </div>
                </div>
            `;
        }).join('');
        
        console.log('Movies rendered successfully');
    } catch (error) {
        console.error('Error loading movies to rate:', error);
        container.innerHTML = `<div class="error">Error loading movies: ${error.message}</div>`;
    }
}

// Rate a movie
async function rateMovie(movieId, rating) {
    console.log('Rating movie:', movieId, 'with', rating, 'stars');
    
    try {
        const response = await fetch('/api/rate_movie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie_id: movieId, rating: rating })
        });
        
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Rating response:', data);
        
        if (response.ok && data.success) {
            // Update stars in the UI
            const starsContainer = document.querySelector(`.rating-stars[data-movie-id="${movieId}"]`);
            if (starsContainer) {
                const stars = starsContainer.querySelectorAll('.star');
                stars.forEach((star, index) => {
                    if (index < rating) {
                        star.classList.add('filled');
                    } else {
                        star.classList.remove('filled');
                    }
                });
            }
            
            // Update rating text
            const ratingText = document.getElementById(`rating-text-${movieId}`);
            if (ratingText) {
                ratingText.textContent = `Your rating: ${rating}/5`;
            }
            
            // Show success message
            showToast('Rating saved! 🎉');
        } else {
            const errorMsg = data.error || data.message || 'Error saving rating';
            console.error('Rating failed:', errorMsg);
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        console.error('Error rating movie:', error);
        showToast('Network error. Please try again.', 'error');
    }
}

// Load my ratings
async function loadMyRatings() {
    const resultsDiv = document.getElementById('ratings-results');
    if (!resultsDiv) return;
    
    resultsDiv.innerHTML = '<div class="loading">⭐ Loading your ratings...</div>';
    
    try {
        const response = await fetch('/api/my_ratings');
        const ratings = await response.json();
        
        console.log('My ratings loaded:', ratings);
        
        if (ratings.error || !Array.isArray(ratings) || ratings.length === 0) {
            resultsDiv.innerHTML = '<div class="info-message"><h3>No ratings yet</h3><p>You haven\'t rated any movies yet. Go to "Rate Movies" tab to start!</p></div>';
            return;
        }
        
        displayRatings(ratings, resultsDiv);
    } catch (error) {
        console.error('Error loading ratings:', error);
        resultsDiv.innerHTML = '<div class="error">Error loading ratings</div>';
    }
}

// Load content-based recommendations
async function loadContentBased() {
    const movieId = document.getElementById('content-movie').value;
    const count = document.getElementById('content-count').value;
    const resultsDiv = document.getElementById('content-results');
    
    if (!movieId) {
        resultsDiv.innerHTML = '';
        return;
    }
    
    resultsDiv.innerHTML = '<div class="loading">🎬 Finding similar movies...</div>';
    
    try {
        const response = await fetch(`/api/recommend/content/${movieId}?n=${count}`);
        const recommendations = await response.json();
        
        if (recommendations.error) {
            resultsDiv.innerHTML = `<div class="error">${recommendations.error}</div>`;
            return;
        }
        
        displayContentRecommendations(recommendations, resultsDiv);
    } catch (error) {
        resultsDiv.innerHTML = '<div class="error">Error loading recommendations</div>';
    }
}

// Display recommendations with scores
function displayRecommendations(recommendations, container) {
    if (recommendations.length === 0) {
        container.innerHTML = '<div class="error">No recommendations found</div>';
        return;
    }
    
    container.innerHTML = recommendations.map((rec, index) => `
        <div class="movie-card" style="animation-delay: ${index * 0.1}s">
            <h3>${index + 1}. ${rec.title}</h3>
            <div class="movie-genres">
                ${rec.genres.split('|').map(genre => 
                    `<span class="genre-tag">${genre}</span>`
                ).join('')}
            </div>
            <div class="movie-score">Score: ${rec.score.toFixed(2)} ⭐</div>
        </div>
    `).join('');
}

// Display content-based recommendations
function displayContentRecommendations(recommendations, container) {
    if (recommendations.length === 0) {
        container.innerHTML = '<div class="error">No recommendations found</div>';
        return;
    }
    
    container.innerHTML = recommendations.map((rec, index) => `
        <div class="movie-card" style="animation-delay: ${index * 0.1}s">
            <h3>${index + 1}. ${rec.title}</h3>
            <div class="movie-genres">
                ${rec.genres.split('|').map(genre => 
                    `<span class="genre-tag">${genre}</span>`
                ).join('')}
            </div>
        </div>
    `).join('');
}

// Display user ratings
function displayRatings(ratings, container) {
    if (ratings.length === 0) {
        container.innerHTML = '<div class="error">No ratings found</div>';
        return;
    }
    
    container.innerHTML = ratings.map((rating, index) => `
        <div class="rating-card" style="animation-delay: ${index * 0.1}s">
            <h3>${rating.title}</h3>
            <div class="movie-genres">
                ${rating.genres.split('|').map(genre => 
                    `<span class="genre-tag">${genre}</span>`
                ).join('')}
            </div>
            <div class="stars">${'⭐'.repeat(rating.rating)} (${rating.rating}/5)</div>
        </div>
    `).join('');
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type === 'error' ? 'toast-error' : ''}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}
