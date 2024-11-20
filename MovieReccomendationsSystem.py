import numpy as np


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


class UserInterface:
    def __init__(self):
        pass
    def run(self):
        pass
def main():
    mv = MovieRecommender()
    mat = np.matrix(mv.movies, mv.ratings)
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