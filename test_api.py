import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("Testing Tamil Movie Recommender API\n")
print("="*50)

# Test 1: Login
print("\n1. Testing Login...")
login_data = {
    "username": "rajesh",
    "password": "pass123"
}

session = requests.Session()
response = session.post(f"{BASE_URL}/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Check session
print("\n2. Checking Session...")
response = session.get(f"{BASE_URL}/api/debug/session")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 3: Get movies
print("\n3. Getting Movies...")
response = session.get(f"{BASE_URL}/api/movies")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    movies = response.json()
    print(f"Movies loaded: {len(movies)}")
    print(f"First 3 movies: {[m['title'] for m in movies[:3]]}")
else:
    print(f"Error: {response.json()}")

# Test 4: Get my ratings
print("\n4. Getting My Ratings...")
response = session.get(f"{BASE_URL}/api/my_ratings")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    ratings = response.json()
    if isinstance(ratings, list):
        print(f"Ratings found: {len(ratings)}")
        for r in ratings[:3]:
            print(f"  - {r['title']}: {r['rating']}★")
    else:
        print(f"Response: {ratings}")
else:
    print(f"Error: {response.json()}")

# Test 5: Rate a movie
print("\n5. Rating a Movie (Leo - ID 21, Rating 5)...")
rate_data = {
    "movie_id": 21,
    "rating": 5
}
response = session.post(f"{BASE_URL}/api/rate_movie", json=rate_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n" + "="*50)
print("✅ API Test Complete!")
