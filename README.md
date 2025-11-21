# 🎬 Tamil Movie Recommendation System

An AI-powered movie recommendation web application that suggests Tamil movies based on user preferences using Machine Learning algorithms.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.7-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- **User Authentication** - Secure signup and login system
- **Interactive Rating System** - Rate movies with animated star ratings
- **AI-Powered Recommendations** - Get personalized movie suggestions
- **Multiple Recommendation Algorithms**:
  - Collaborative Filtering (User-based)
  - Content-Based Filtering (Genre-based)
  - Hybrid Approach (Best of both worlds)
- **Beautiful UI** - Colorful, animated, and responsive design
- **Real-time Updates** - Instant recommendation updates as you rate

## 🤖 AI/ML Techniques Used

### 1. Collaborative Filtering
- Uses **Cosine Similarity** to find users with similar taste
- Predicts ratings based on similar users' preferences
- Implements user-based collaborative filtering

### 2. Content-Based Filtering
- Uses **CountVectorizer** (NLP) to analyze movie genres
- Calculates similarity between movies based on features
- Recommends movies with similar characteristics

### 3. Hybrid Recommendation
- Combines collaborative and content-based approaches
- Applies genre-based boosting for better accuracy
- Ensemble learning technique for optimal results

## 📊 Technologies

- **Backend**: Flask (Python)
- **ML Libraries**: scikit-learn, NumPy, Pandas
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: CSV files (easily upgradable to SQL)

## 🚀 Installation

### Prerequisites
- Python 3.13 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/tamil-movie-recommender.git
cd tamil-movie-recommender
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://localhost:5000
```

## 📖 Usage

### For New Users

1. **Sign Up**: Create a new account
2. **Rate Movies**: Go to "Rate Movies" tab and rate at least 3-5 movies
3. **Get Recommendations**: Check "My Recommendations" for personalized suggestions

### Demo Accounts

- Username: `rajesh` | Password: `pass123`
- Username: `priya` | Password: `pass123`

## 🎯 How It Works

### Recommendation Pipeline

```
User Ratings → Data Processing → ML Algorithms → Personalized Recommendations
                                      ↓
                    ┌─────────────────┴─────────────────┐
                    ↓                                   ↓
          Collaborative Filtering              Content-Based Filtering
          (Similar Users)                      (Similar Genres)
                    ↓                                   ↓
                    └─────────────────┬─────────────────┘
                                      ↓
                              Hybrid Algorithm
                                      ↓
                          Final Recommendations
```

### Algorithm Details

**Collaborative Filtering:**
- Creates user-movie rating matrix
- Computes cosine similarity between users
- Predicts ratings for unrated movies

**Content-Based Filtering:**
- Extracts genre features using CountVectorizer
- Calculates movie similarity matrix
- Recommends movies with similar genres

**Hybrid Approach:**
- Combines both algorithms
- Boosts scores for movies matching user's favorite genres
- Provides diverse and accurate recommendations

## 📁 Project Structure

```
tamil-movie-recommender/
├── app.py                      # Flask application
├── recommendation_system.py    # ML recommendation engine
├── requirements.txt            # Python dependencies
├── movies_data.csv            # Movie database (23 Tamil movies)
├── user_ratings.csv           # User ratings data
├── users.csv                  # User accounts
├── templates/
│   ├── index.html            # Main application page
│   ├── login.html            # Login page
│   └── signup.html           # Signup page
└── static/
    ├── style.css             # Main styles
    ├── auth.css              # Authentication styles
    └── script.js             # Frontend JavaScript

```

## 🎬 Movie Database

The system includes 23 popular Tamil movies across various genres:

- **Action**: Baahubali, Vikram, Leo, Thuppakki
- **Drama**: 96, Jai Bhim, Soorarai Pottru, Karnan
- **Romance**: Roja, Bombay
- **Crime**: Nayakan, Vada Chennai, Visaranai
- **Biography**: MS Dhoni: The Untold Story
- **And more!**

## 🔧 Configuration

### Adding More Movies

Edit `movies_data.csv`:
```csv
movie_id,title,genres
24,Your Movie,Action|Drama
```

### Customizing Recommendations

In `recommendation_system.py`, adjust:
- Number of similar users: `similar_users.index[:3]`
- Genre boost factor: `len(common_genres) * 0.1`
- Minimum rating threshold: `user_ratings[user_ratings['rating'] >= 4]`

## 🎨 UI Features

- **Animated gradient background** that shifts colors
- **Glassmorphism effects** with blur and transparency
- **Smooth animations** for cards, stars, and buttons
- **Interactive star ratings** with rotation and glow effects
- **Toast notifications** for user feedback
- **Fully responsive** design for all devices

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Sanjay Balan M**
- GitHub: [@sanjaybalanm](https://github.com/sanjaybalanm)

## 🙏 Acknowledgments

- Movie data curated from popular Tamil cinema
- Built with Flask and scikit-learn
- Inspired by Netflix and Spotify recommendation systems

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ If you found this project helpful, please give it a star!
