import unittest
import pandas as pd
import numpy as np
from MovieReccomendationsSystem import MovieRecommender
class TestMovieRecommender(unittest.TestCase):
    def setUp(self):
        self.recommender = MovieRecommender()
        self.recommender.calculate_similarity()

    def test_similarity_matrix_shape(self):
        self.assertEqual(
            self.recommender.similarity_matrix.shape,
            (self.recommender.user_movie_matrix.shape[0], self.recommender.user_movie_matrix.shape[0])
        )

    def test_recommend_movies(self):
        recommendations = self.recommender.recommend_movies(1, top_n=3)
        self.assertEqual(len(recommendations), 3)
        self.assertTrue(all(isinstance(movie, str) for movie in recommendations))

    def test_no_ratings_for_user(self):
        """Test the case where a user has no ratings."""
        # Create a mock user with no ratings
        self.recommender.user_movie_matrix[0, :] = 0  # First user with no ratings
        recommendations = self.recommender.recommend_movies(1, top_n=3)
        self.assertEqual(recommendations, [])

    def test_missing_movie_data(self):
        """Test case where movie data is missing for some movie ID."""
        # Simulate a missing movieId by modifying the movies DataFrame
        missing_movie_id = 9999  # Assume this ID doesn't exist in the 'movies' dataset
        recommendations = self.recommender.recommend_movies(1, top_n=3)
        # Make sure that no recommendation is for a missing movie
        self.assertNotIn(missing_movie_id, [movie_id for movie_id, _ in recommendations])

    def test_edge_case_zero_ratings(self):
        """Test case where all user ratings are zero (shouldn't generate recommendations)."""
        self.recommender.user_movie_matrix[1, :] = 0  # Second user with all zero ratings
        recommendations = self.recommender.recommend_movies(2, top_n=3)
        self.assertEqual(recommendations, [])

    def test_similarity_for_known_data(self):
        """Test the cosine similarity calculation with known values."""
        # Use a small matrix for testing
        small_matrix = np.array([[5, 3, 0, 1],
                                 [4, 0, 0, 1],
                                 [1, 1, 0, 5],
                                 [1, 0, 0, 4]])

        # Manually calculate similarity for testing
        recommender = MovieRecommender()
        recommender.user_movie_matrix = pd.DataFrame(small_matrix)
        recommender.calculate_similarity()

        # Cosine similarity between the first and second user (should be positive)
        similarity = recommender.similarity_matrix[0, 1]
        self.assertGreater(similarity, 0)

    def test_empty_movie_list(self):
        """Test case where the movie list is empty."""
        self.recommender.movies = pd.DataFrame(columns=['movieId', 'title'])
        recommendations = self.recommender.recommend_movies(1, top_n=3)
        self.assertEqual(recommendations, [])

if __name__ == "__main__":
    unittest.main()