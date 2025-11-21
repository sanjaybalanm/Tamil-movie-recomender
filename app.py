from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from recommendation_system import MovieRecommender
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'tamil_movie_recommender_secret_key_2024'
recommender = MovieRecommender()

# Load users data
USERS_FILE = 'users.csv'
if os.path.exists(USERS_FILE):
    users_df = pd.read_csv(USERS_FILE)
else:
    users_df = pd.DataFrame(columns=['user_id', 'username', 'password', 'email'])
    users_df.to_csv(USERS_FILE, index=False)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        global users_df
        users_df = pd.read_csv(USERS_FILE)
        
        user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
        
        if not user.empty:
            session['user_id'] = int(user.iloc[0]['user_id'])
            session['username'] = username
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        global users_df
        users_df = pd.read_csv(USERS_FILE)
        
        if username in users_df['username'].values:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        new_user_id = users_df['user_id'].max() + 1 if not users_df.empty else 1
        new_user = pd.DataFrame([{
            'user_id': new_user_id,
            'username': username,
            'password': password,
            'email': email
        }])
        
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(USERS_FILE, index=False)
        
        session['user_id'] = int(new_user_id)
        session['username'] = username
        
        return jsonify({'success': True, 'message': 'Signup successful', 'user_id': int(new_user_id)})
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/users')
def get_users():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    users = recommender.ratings['user_id'].unique().tolist()
    return jsonify(users)


@app.route('/api/current_user')
def get_current_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated', 'session': dict(session)}), 401
    return jsonify({
        'user_id': session['user_id'],
        'username': session['username']
    })


@app.route('/api/debug/session')
def debug_session():
    return jsonify({
        'session': dict(session),
        'has_user_id': 'user_id' in session,
        'user_id': session.get('user_id'),
        'username': session.get('username')
    })


@app.route('/api/movies')
def get_movies():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    movies = recommender.movies.to_dict('records')
    # Convert int64 to int for JSON serialization
    for movie in movies:
        movie['movie_id'] = int(movie['movie_id'])
    return jsonify(movies)


@app.route('/api/rate_movie', methods=['POST'])
def rate_movie():
    try:
        print("Rate movie endpoint called")
        
        if 'user_id' not in session:
            print("User not authenticated")
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        data = request.json
        user_id = session['user_id']
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        
        print(f"User {user_id} rating movie {movie_id} with {rating} stars")
        
        # Validate inputs
        if not movie_id or not rating:
            return jsonify({'success': False, 'error': 'Missing movie_id or rating'}), 400
        
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'error': 'Rating must be between 1 and 5'}), 400
        
        # Load current ratings
        ratings_df = pd.read_csv('user_ratings.csv')
        
        # Check if user already rated this movie
        existing = ratings_df[(ratings_df['user_id'] == user_id) & (ratings_df['movie_id'] == movie_id)]
        
        if not existing.empty:
            # Update existing rating
            print(f"Updating existing rating")
            ratings_df.loc[(ratings_df['user_id'] == user_id) & (ratings_df['movie_id'] == movie_id), 'rating'] = rating
        else:
            # Add new rating
            print(f"Adding new rating")
            new_rating = pd.DataFrame([{
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': rating
            }])
            ratings_df = pd.concat([ratings_df, new_rating], ignore_index=True)
        
        # Save to CSV
        ratings_df.to_csv('user_ratings.csv', index=False)
        print("Rating saved to CSV")
        
        # Reload recommender data
        recommender._load_data()
        print("Recommender data reloaded")
        
        return jsonify({'success': True, 'message': 'Rating saved successfully!'})
    
    except Exception as e:
        print(f"Error in rate_movie: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/user/<int:user_id>/ratings')
def get_user_ratings(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    ratings = recommender.get_user_ratings(user_id)
    return jsonify(ratings)


@app.route('/api/my_ratings')
def get_my_ratings():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    ratings = recommender.get_user_ratings(session['user_id'])
    return jsonify(ratings)


@app.route('/api/recommend/collaborative/<int:user_id>')
def collaborative_recommend(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    n = request.args.get('n', default=5, type=int)
    recommendations = recommender.collaborative_filtering(user_id, n)
    
    if isinstance(recommendations, str):
        return jsonify({'error': recommendations}), 404
    
    result = [
        {
            'movie_id': movie_id,
            'title': title,
            'genres': genres,
            'score': score
        }
        for movie_id, title, genres, score in recommendations
    ]
    return jsonify(result)


@app.route('/api/recommend/my_recommendations')
def my_recommendations():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    n = request.args.get('n', default=5, type=int)
    
    # Check if user has ratings
    user_ratings = recommender.get_user_ratings(user_id)
    if isinstance(user_ratings, str) or len(user_ratings) == 0:
        return jsonify({'error': 'Please rate some movies first to get recommendations'}), 404
    
    recommendations = recommender.hybrid_recommendation(user_id, n)
    
    if isinstance(recommendations, str):
        return jsonify({'error': recommendations}), 404
    
    result = [
        {
            'movie_id': movie_id,
            'title': title,
            'genres': genres,
            'score': score
        }
        for movie_id, title, genres, score in recommendations
    ]
    return jsonify(result)


@app.route('/api/recommend/content/<int:movie_id>')
def content_recommend(movie_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    n = request.args.get('n', default=5, type=int)
    recommendations = recommender.content_based_filtering(movie_id, n)
    
    if isinstance(recommendations, str):
        return jsonify({'error': recommendations}), 404
    
    result = recommendations.to_dict('records')
    # Convert int64 to int for JSON serialization
    for rec in result:
        rec['movie_id'] = int(rec['movie_id'])
    return jsonify(result)


@app.route('/api/recommend/hybrid/<int:user_id>')
def hybrid_recommend(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    n = request.args.get('n', default=5, type=int)
    recommendations = recommender.hybrid_recommendation(user_id, n)
    
    if isinstance(recommendations, str):
        return jsonify({'error': recommendations}), 404
    
    result = [
        {
            'movie_id': movie_id,
            'title': title,
            'genres': genres,
            'score': score
        }
        for movie_id, title, genres, score in recommendations
    ]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
