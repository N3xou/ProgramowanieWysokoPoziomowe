import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, ratings_file='ratings.dat', movies_file='movies.dat'):
        # Wczytanie danych z plików
        self.ratings_file = ratings_file
        self.movies_file = movies_file

        try:
            self.ratings = pd.read_csv(
                self.ratings_file,
                sep="::",
                names=["userId", "movieId", "rating", "timestamp"],
                encoding="ISO-8859-1",
                engine='python'
            ).drop(columns=["timestamp"])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {ratings_file} not found.")

        try:
            self.movies = pd.read_csv(
                self.movies_file,
                sep="::",
                names=["movieId", "title", "genres"],
                encoding="ISO-8859-1",
                engine='python'
            ).drop(columns=["genres"])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {movies_file} not found.")

        # Utwórz macierz użytkownik-film
        self.user_movie_matrix = self.ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
        self.similarity_matrix = None
        print(self.user_movie_matrix.head())

    def calculate_similarity(self):
        """
        Oblicza podobieństwo między użytkownikami za pomocą cosine similarity.
        """
        self.similarity_matrix = cosine_similarity(self.user_movie_matrix)
        return self.similarity_matrix

    import numpy as np
    import pandas as pd
    from sklearn.metrics.pairwise import cosine_similarity

    class MovieRecommender:
        def __init__(self, ratings_file='ratings.dat', movies_file='movies.dat'):
            # Wczytanie danych z plików
            self.ratings_file = ratings_file
            self.movies_file = movies_file

            # Wczytaj dane wejściowe
            try:
                self.ratings = pd.read_csv(
                    self.ratings_file,
                    sep="::",
                    names=["userId", "movieId", "rating", "timestamp"],
                    encoding="ISO-8859-1",
                    engine='python'
                ).drop(columns=["timestamp"])
            except FileNotFoundError:
                raise FileNotFoundError(f"File {ratings_file} not found.")

            try:
                self.movies = pd.read_csv(
                    self.movies_file,
                    sep="::",
                    names=["movieId", "title", "genres"],
                    encoding="ISO-8859-1",
                    engine='python'
                ).drop(columns=["genres"])
            except FileNotFoundError:
                raise FileNotFoundError(f"File {movies_file} not found.")

            # Utwórz macierz użytkownik-film
            self.user_movie_matrix = self.ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
            self.similarity_matrix = None

        def calculate_similarity(self):
            """
            Oblicza podobieństwo między użytkownikami za pomocą cosine similarity.
            """
            self.similarity_matrix = cosine_similarity(self.user_movie_matrix)
            return self.similarity_matrix

        def recommend_movies(self, user_id, top_n=5):
            """
            Rekomenduje filmy na podstawie ocen podobnych użytkowników.
            :param user_id: ID użytkownika.
            :param top_n: Liczba rekomendacji.
            :return: Lista rekomendowanych filmów.
            """
            if self.similarity_matrix is None:
                raise ValueError("Similarity matrix not computed. Run calculate_similarity() first.")

            user_index = user_id - 1  # Indeks użytkownika (zakładając indeksowanie od 1)
            similar_users = self.similarity_matrix[user_index]

            # Sortowanie podobieństwa i wybór użytkowników podobnych
            similar_users_indices = np.argsort(-similar_users)  # Posortuj w kolejności malejącej
            recommendations = {}

            # Pobierz oceny podobnych użytkowników
            for idx in similar_users_indices[1:]:
                user_ratings = self.user_movie_matrix.iloc[idx]
                for movie_id, rating in user_ratings.items():
                    if self.user_movie_matrix.iloc[user_index, movie_id] == 0 and rating > 0:
                        if movie_id not in recommendations:
                            recommendations[movie_id] = rating
                        else:
                            recommendations[movie_id] += rating

            # Posortuj rekomendacje po najwyższej ocenie
            recommended_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
            return [(self.movies[self.movies['movieId'] == movie_id]['title'].values[0], score) for movie_id, score in
                    recommended_movies]


class UserInterface:
    def __init__(self):
        pass
    def run(self):
        pass
def main():
    mv = MovieRecommender()
    mat = np.matrix()
if __name__ == '__main__':
    main()


#Użyj plików DAT, które zawierają (UWAGA! Kodowanie plików ISO-8859-1):
#• ratings.dat: Dane z ocenami filmów przez użytkowników: example data '6040::1089::4::956704996'
#• userId: ID użytkownika.
#• movieId: ID filmu.
#• rating: Ocena filmu (1-5).
#• movies.dat: Dane z tytułami filmów: example data '3885::Love & Sex (2000)::Comedy|Romance'
#• movieId: ID filmu.
#• title: Tytuł filmu.
# genre