import unittest
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


if __name__ == "__main__":
    unittest.main()