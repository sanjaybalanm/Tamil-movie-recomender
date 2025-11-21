import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class MovieRecommender:
    def __init__(self, movies_file='movies_data.csv', ratings_file='user_ratings.csv'):
        self.movies_file = movies_file
        self.ratings_file = ratings_file
        self._load_data()
    
    def _load_data(self):
        """Load or reload data from CSV files"""
        self.movies = pd.read_csv(self.movies_file)
        self.ratings = pd.read_csv(self.ratings_file)
        self.user_movie_matrix = None
        self.content_similarity = None
        self._prepare_data()
    
    def _prepare_data(self):
        # Create user-movie rating matrix for collaborative filtering
        self.user_movie_matrix = self.ratings.pivot_table(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
        
        # Calculate content-based similarity
        cv = CountVectorizer(tokenizer=lambda x: x.split('|'))
        genre_matrix = cv.fit_transform(self.movies['genres'])
        self.content_similarity = cosine_similarity(genre_matrix)
    
    def collaborative_filtering(self, user_id, n_recommendations=5):
        """Recommend movies based on similar users' preferences"""
        if user_id not in self.user_movie_matrix.index:
            return "User not found"
        
        # Calculate user similarity
        user_similarity = cosine_similarity(self.user_movie_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity,
            index=self.user_movie_matrix.index,
            columns=self.user_movie_matrix.index
        )
        
        # Get similar users (excluding the user itself)
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]
        
        # Get movies the user hasn't rated
        user_ratings = self.user_movie_matrix.loc[user_id]
        unrated_movies = user_ratings[user_ratings == 0].index
        
        # Calculate weighted ratings from similar users
        recommendations = {}
        for movie_id in unrated_movies:
            weighted_sum = 0
            similarity_sum = 0
            
            for similar_user_id in similar_users.index[:3]:  # Top 3 similar users
                rating = self.user_movie_matrix.loc[similar_user_id, movie_id]
                if rating > 0:
                    similarity = similar_users[similar_user_id]
                    weighted_sum += rating * similarity
                    similarity_sum += similarity
            
            if similarity_sum > 0:
                recommendations[movie_id] = weighted_sum / similarity_sum
        
        # Get top N recommendations
        top_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        return self._format_recommendations(top_movies)
    
    def content_based_filtering(self, movie_id, n_recommendations=5):
        """Recommend movies similar to a given movie based on genres"""
        if movie_id not in self.movies['movie_id'].values:
            return "Movie not found"
        
        # Get movie index
        movie_idx = self.movies[self.movies['movie_id'] == movie_id].index[0]
        
        # Get similarity scores
        similarity_scores = list(enumerate(self.content_similarity[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:]
        
        # Get top N similar movies
        top_indices = [i[0] for i in similarity_scores[:n_recommendations]]
        recommended_movies = self.movies.iloc[top_indices][['movie_id', 'title', 'genres']]
        
        return recommended_movies
    
    def hybrid_recommendation(self, user_id, n_recommendations=5):
        """Combine collaborative and content-based filtering"""
        collab_recs = self.collaborative_filtering(user_id, n_recommendations * 2)
        
        if isinstance(collab_recs, str):
            return collab_recs
        
        # Get user's favorite genres from their ratings
        user_ratings = self.ratings[self.ratings['user_id'] == user_id]
        favorite_movies = user_ratings[user_ratings['rating'] >= 4]['movie_id'].values
        
        hybrid_scores = {}
        for movie_id, title, genres, score in collab_recs:
            # Boost score if movie shares genres with user's favorites
            movie_genres = self.movies[self.movies['movie_id'] == movie_id]['genres'].values[0]
            genre_match = 0
            
            for fav_movie_id in favorite_movies:
                fav_genres = self.movies[self.movies['movie_id'] == fav_movie_id]['genres'].values[0]
                common_genres = set(movie_genres.split('|')) & set(fav_genres.split('|'))
                genre_match += len(common_genres) * 0.1
            
            hybrid_scores[movie_id] = score + genre_match
        
        top_movies = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        return self._format_recommendations(top_movies)
    
    def _format_recommendations(self, movie_scores):
        """Format movie recommendations with titles and genres"""
        recommendations = []
        for movie_id, score in movie_scores:
            movie_info = self.movies[self.movies['movie_id'] == movie_id].iloc[0]
            recommendations.append((movie_id, movie_info['title'], movie_info['genres'], round(score, 2)))
        return recommendations
    
    def get_movie_info(self, movie_id):
        """Get information about a specific movie"""
        movie = self.movies[self.movies['movie_id'] == movie_id]
        if movie.empty:
            return "Movie not found"
        return movie.iloc[0].to_dict()
    
    def get_user_ratings(self, user_id):
        """Get all ratings for a specific user"""
        user_ratings = self.ratings[self.ratings['user_id'] == user_id]
        if user_ratings.empty:
            return "User not found"
        
        result = []
        for _, row in user_ratings.iterrows():
            movie_info = self.movies[self.movies['movie_id'] == row['movie_id']].iloc[0]
            result.append({
                'title': str(movie_info['title']),
                'genres': str(movie_info['genres']),
                'rating': int(row['rating'])  # Convert to Python int
            })
        return result
