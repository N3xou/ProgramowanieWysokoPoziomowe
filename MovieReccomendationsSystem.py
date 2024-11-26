import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    """
       System rekomendacji filmów oparty na filtracji opartej na współpracy użytkowników.

       Attributes:
           ratings_file (str): Ścieżka do pliku z ocenami użytkowników.
           movies_file (str): Ścieżka do pliku z informacjami o filmach.
           ratings (pd.DataFrame): Dane o ocenach użytkowników.
           movies (pd.DataFrame): Dane o filmach.
           user_movie_matrix (pd.DataFrame): Macierz użytkownik-film.
           similarity_matrix (np.ndarray): Macierz podobieństwa użytkowników.
       """
    def __init__(self, ratings_file='ratings.dat', movies_file='movies.dat'):
        """
               Inicjalizuje system rekomendacji, wczytuje dane i tworzy macierz użytkownik-film.

               Args:
                   ratings_file (str): Ścieżka do pliku z ocenami użytkowników. Domyślnie 'ratings.dat'.
                   movies_file (str): Ścieżka do pliku z informacjami o filmach. Domyślnie 'movies.dat'.
               """
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
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"File {movies_file} not found.")

        # Utwórz macierz użytkownik-film
        self.user_movie_matrix = self.ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
        self.similarity_matrix = None

    def calculate_similarity(self):
        """
                Oblicza macierz podobieństwa użytkowników za pomocą podobieństwa cosinusowego.

                Returns:
                    np.ndarray: Macierz podobieństwa użytkowników.
                """
        self.similarity_matrix = cosine_similarity(self.user_movie_matrix)
        return self.similarity_matrix

    def recommend_movies(self, user_id, top_n=5, sort_by = 'score', genre = None):
        """
        Rekomenduje filmy dla podanego użytkownika na podstawie ocen podobnych użytkowników.

        Args:
            user_id (int): ID użytkownika, dla którego generowane są rekomendacje.
            top_n (int): Liczba rekomendowanych filmów. Domyślnie 5.
            genre (str): Gatunki do filtrowania wyników (np. 'Comedy Drama').
            sort_by(str): Sposób sortowania (title,genre,score). Domyślnie score

        Returns:
            list: Lista rekomendowanych filmów w formacie (tytuł, gatunki, trafność).
        """
        if user_id not in self.user_movie_matrix.index:
            raise ValueError("User ID not found")
        if self.similarity_matrix is None:
            raise ValueError("Podobienstwa nie sa obliczone, najpierw oblicz podobienstwa.")

        user_index = user_id - 1  # assuming indexing starting from 1
        user_ratings = self.user_movie_matrix.loc[user_id]

        # If the user has no ratings, return an empty list
        if user_ratings.sum() == 0:
            return []
        similar_users = self.similarity_matrix[user_index]
        similar_users_indices = np.argsort(-similar_users)  # Posortuj w kolejności malejącej
        recommendations = {}

            # Pobierz oceny podobnych użytkowników
        for idx in similar_users_indices[1:100]:
            similar_user_ratings = self.user_movie_matrix.iloc[idx]
            for movie_id, rating in similar_user_ratings.items():
                if self.user_movie_matrix.at[user_id, movie_id] == 0 and rating > 0: #  reccomends unwatched by user movies
                    if movie_id not in recommendations:
                        recommendations[movie_id] = rating
                    else:
                        recommendations[movie_id] += rating

            # Posortuj rekomendacje po najwyższej ocenie
        #recommended_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
        movie_titles = []
        genre_filters = genre.lower().split() if genre else []  # Split input into a list of genres
        for movie_id, score in recommendations.items():
            # Ensure the movie_id exists in self.movies before attempting access
            movie_row = self.movies[self.movies['movieId'] == movie_id]
            if not movie_row.empty:
                title = movie_row['title'].values[0]
                genres = movie_row['genres'].values[0].lower()

                # Check if all genres in genre_filters are in the movie's genres
                if all(genre in genres for genre in genre_filters):
                    movie_titles.append((title, genres, score))

        if sort_by == 'title':
            movie_titles.sort(key=lambda x: x[0])
        elif sort_by == 'genre':
            movie_titles.sort(key=lambda x: x[1])
        elif sort_by == 'score':
            movie_titles.sort(key=lambda x: x[2], reverse=True)
        # sorting by score
        return movie_titles[:top_n]

    def get_all_genres(self):
        """Funkcja która zwraca zbiór dostępnych gatunków filmowych.
        Returns:
            set: Zbiór dostępnych gatunków

        """
        # w set dane nie moga sie powtarzac, w liscie moga
        genres = set()
        for genre_list in self.movies['genres']:
            genres.update(genre_list.split('|'))
        return sorted(genres)


class UserInterface:
    """
    Interfejs użytkownika do obsługi systemu rekomendacji filmów.
    """
    def __init__(self, movie_recommender):
        """
        Inicjalizuje interfejs użytkownika.

        Args:
            movie_recommender (MovieRecommender): Instancja systemu rekomendacji.
        """
        self.movie_recommender = movie_recommender

    def run(self):
        """
        Uruchamia interfejs użytkownika, umożliwiając interakcję z systemem rekomendacji.
        """
        while True:
            print("\nOpcje:")
            print("1. Oblicz podobieństwo między użytkownikami")
            print("2. Zaproponuj filmy")
            print("3. Wyświetl dostępne gatunki filmowe")
            print("4. Wyjście z programu")

            choice = input("Wybierz opcję (1-4): ")

            if choice == "1":
                print("Obliczanie podobieństwa między użytkownikami...")
                self.movie_recommender.calculate_similarity()
                print("Podobieństwo zostało obliczone.")
            elif choice == "2":
                try:
                    user_id = int(input("Podaj ID użytkownika: "))
                    genre_filter = input("Podaj gatunek (naciśnij Enter aby pominąć): ")
                    sort_by = input("Sortuj wyniki według (title, genre, score.) [Domyślnie score:trafność]: ").strip().lower()
                    amt_recommendations = int(input("Ile wyników chcesz wyświetlić?:  "))
                    if amt_recommendations <= 0:
                        amt_recommendations = 1
                    if sort_by not in ['title', 'genre', 'score']:
                        sort_by = 'score'

                    print(f"Rekomendacje dla użytkownika {user_id}:")
                    recommendations = self.movie_recommender.recommend_movies(
                        user_id=user_id,
                        genre=genre_filter if genre_filter else None,
                        sort_by=sort_by,
                        top_n = amt_recommendations
                    )
                    for title, genre, score in recommendations:
                        print(f"{title} | Gatunek: {genre} | Trafność: {score:.2f}")
                except ValueError:
                    print("Błąd: Wprowadź poprawne dane.")
                except Exception as e:
                    print(f"Wystąpił błąd: {e}")
            elif choice == "3":
                genres = self.movie_recommender.get_all_genres()
                print("\nDostępne gatunki filmowe:")
                for genre in genres:
                    print(f"- {genre}")
            elif choice == "4":
                print("Dziękujemy za skorzystanie z systemu rekomendacji. Do widzenia!")
                break
            else:
                print("Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    mv = MovieRecommender()
    ui = UserInterface(mv)
    ui.run()


#Użyj plików DAT, które zawierają (UWAGA! Kodowanie plików ISO-8859-1):
#• ratings.dat: Dane z ocenami filmów przez użytkowników: example data '6040::1089::4::956704996'
#• userId: ID użytkownika.
#• movieId: ID filmu.
#• rating: Ocena filmu (1-5).
#• movies.dat: Dane z tytułami filmów: example data '3885::Love & Sex (2000)::Comedy|Romance'
#• movieId: ID filmu.
#• title: Tytuł filmu.
# genre
# todo: check if multiple genres can be added and filtered at the same time
# todo: right now program first finds 5 results then filters. so instead of displaying proper 5 results it can only show 1 as the other 4 get filtered due to genre
# todo: change program to filter first and then find 5 results