import numpy as np
class MovieRecommender:
    def __init__(self):
        try:
            with open('movies.dat', 'r') as file:
                self.movies = file.read()
        except FileNotFoundError:
            print('movies.dat file not found')
        try:
            with open('ratings.dat', 'r') as file:
                self.ratings = file.read()
        except FileNotFoundError:
            print('ratings.dat file not found')

    def calculate_similiarity(self):
        pass
        #Program umożliwia obliczenie macierzy podobieństwa użytkowników przy użyciu cosine similarity
    def reccomend_movies(self):
        pass

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