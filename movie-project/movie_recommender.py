"""
Movie Recommendation System using Collaborative Filtering
Memory-safe version for normal laptops

Author: Your Name
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Load datasets (LIMITED SIZE)
# -----------------------------
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")

# 🔒 LIMIT DATASET to avoid memory error
ratings = ratings.head(5000)          # safe limit
ratings = ratings[ratings["userId"] <= 100]  # limit users


# -----------------------------
# Create User-Movie Matrix
# -----------------------------
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)


# -----------------------------
# Compute User Similarity
# -----------------------------
user_similarity = cosine_similarity(user_movie_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)


# -----------------------------
# Recommendation Function
# -----------------------------
def recommend_movies(user_id, num_recommendations=3):
    if user_id not in user_movie_matrix.index:
        print("User not found")
        return

    # Get similar users (excluding self)
    similar_users = user_similarity_df[user_id].sort_values(
        ascending=False
    )[1:4]

    # Weighted ratings
    weighted_ratings = np.zeros(len(user_movie_matrix.columns))

    for sim_user, similarity in similar_users.items():
        weighted_ratings += similarity * user_movie_matrix.loc[sim_user].values

    weighted_ratings /= similar_users.sum()

    # Create recommendations DataFrame
    recommendations = pd.DataFrame({
        "movieId": user_movie_matrix.columns,
        "score": weighted_ratings
    })

    # Remove watched movies
    watched = user_movie_matrix.loc[user_id]
    watched_movies = watched[watched > 0].index

    recommendations = recommendations[
        ~recommendations["movieId"].isin(watched_movies)
    ]

    # Top recommendations
    top_movies = recommendations.sort_values(
        by="score",
        ascending=False
    ).head(num_recommendations)

    print("\n🎬 Recommended Movies:")
    for title in movies[movies["movieId"].isin(top_movies["movieId"])]["title"]:
        print(title)


# -----------------------------
# Run the System
# -----------------------------
recommend_movies(1)
