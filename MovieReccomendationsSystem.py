
class MovieRecommender:
    def __init__(self):

        with open('movies.dat', 'r') as file:
            content = file.read()
            print(content)
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

mv = MovieRecommender
#Użyj plików DAT, które zawierają (UWAGA! Kodowanie plików ISO-8859-1):
#• ratings.dat: Dane z ocenami filmów przez użytkowników:
#• userId: ID użytkownika.
#• movieId: ID filmu.
#• rating: Ocena filmu (1-5).
#• movies.dat: Dane z tytułami filmów:
#• movieId: ID filmu.
#• title: Tytuł filmu.
