from recommendation_system import MovieRecommender


def print_recommendations(recommendations, method_name):
    print(f"\n{'='*60}")
    print(f"{method_name}")
    print(f"{'='*60}")
    
    if isinstance(recommendations, str):
        print(recommendations)
        return
    
    if isinstance(recommendations, list):
        for i, (movie_id, title, genres, score) in enumerate(recommendations, 1):
            print(f"{i}. {title}")
            print(f"   Genres: {genres}")
            print(f"   Score: {score}\n")
    else:
        print(recommendations)


def main():
    # Initialize the recommender system
    recommender = MovieRecommender()
    
    print("🎬 Movie Recommendation System")
    print("="*60)
    
    # Example 1: Collaborative Filtering
    user_id = 1
    print(f"\nUser {user_id}'s rated movies:")
    user_ratings = recommender.get_user_ratings(user_id)
    for rating in user_ratings:
        print(f"  - {rating['title']} ({rating['genres']}): {rating['rating']}★")
    
    collab_recs = recommender.collaborative_filtering(user_id, n_recommendations=3)
    print_recommendations(collab_recs, f"Collaborative Filtering Recommendations for User {user_id}")
    
    # Example 2: Content-Based Filtering
    movie_id = 1  # The Matrix
    movie_info = recommender.get_movie_info(movie_id)
    print(f"\nBased on: {movie_info['title']} ({movie_info['genres']})")
    
    content_recs = recommender.content_based_filtering(movie_id, n_recommendations=3)
    print(f"\n{'='*60}")
    print("Content-Based Filtering Recommendations")
    print(f"{'='*60}")
    for i, row in content_recs.iterrows():
        print(f"{i+1}. {row['title']}")
        print(f"   Genres: {row['genres']}\n")
    
    # Example 3: Hybrid Recommendation
    hybrid_recs = recommender.hybrid_recommendation(user_id, n_recommendations=3)
    print_recommendations(hybrid_recs, f"Hybrid Recommendations for User {user_id}")
    
    # Interactive mode
    print("\n" + "="*60)
    print("Try it yourself!")
    print("="*60)
    print("\nAvailable commands:")
    print("1. Get recommendations for a user (collaborative)")
    print("2. Get similar movies (content-based)")
    print("3. Get hybrid recommendations")
    print("4. View user ratings")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                user_id = int(input("Enter user ID (1-5): "))
                n = int(input("Number of recommendations (default 5): ") or 5)
                recs = recommender.collaborative_filtering(user_id, n)
                print_recommendations(recs, f"Recommendations for User {user_id}")
            
            elif choice == '2':
                movie_id = int(input("Enter movie ID (1-10): "))
                n = int(input("Number of recommendations (default 5): ") or 5)
                recs = recommender.content_based_filtering(movie_id, n)
                print(f"\n{'='*60}")
                print(f"Movies similar to: {recommender.get_movie_info(movie_id)['title']}")
                print(f"{'='*60}")
                for i, row in recs.iterrows():
                    print(f"{i+1}. {row['title']} - {row['genres']}")
            
            elif choice == '3':
                user_id = int(input("Enter user ID (1-5): "))
                n = int(input("Number of recommendations (default 5): ") or 5)
                recs = recommender.hybrid_recommendation(user_id, n)
                print_recommendations(recs, f"Hybrid Recommendations for User {user_id}")
            
            elif choice == '4':
                user_id = int(input("Enter user ID (1-5): "))
                ratings = recommender.get_user_ratings(user_id)
                print(f"\nUser {user_id}'s Ratings:")
                for rating in ratings:
                    print(f"  - {rating['title']}: {rating['rating']}★")
            
            elif choice == '5':
                print("\nThanks for using the Movie Recommendation System!")
                break
            
            else:
                print("Invalid choice. Please enter 1-5.")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
