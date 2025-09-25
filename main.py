import json

# Custom exception
class MovieNotFoundError(Exception):
    pass

class MovieManager:
    def __init__(self, filename="movies.json"):
        self.filename = filename
        self.movies = []
        self.load_movies()

    def load_movies(self):
        """Načte filmy ze souboru"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        except FileNotFoundError:
            print("Soubor neexistuje, vytvářím nový.")
            self.movies = []
        except json.JSONDecodeError:
            print("Chyba v souboru – špatný JSON formát.")
            self.movies = []

    def save_movies(self):
        """Uloží filmy do souboru"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Nepodařilo se uložit soubor: {e}")

    def add_movie(self, title, year, rating):
        try:
            year = int(year)
            rating = float(rating)
        except ValueError:
            print("Rok musí být číslo a hodnocení číslo.")
            return

        self.movies.append({"title": title, "year": year, "rating": rating})
        print(f"Film '{title}' přidán.")
        self.save_movies()

    def get_movie(self, title):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                return movie
        raise MovieNotFoundError(f"Film '{title}' nebyl nalezen.")

    def calculate_average_rating(self):
        try:
            total = sum(movie["rating"] for movie in self.movies)
            avg = total / len(self.movies)
            return round(avg, 2)
        except ZeroDivisionError:
            print("Nelze počítat průměr, nejsou žádné filmy.")
            return None

if __name__ == "__main__":
    manager = MovieManager()

    while True:
        print("\nMovie Manager")
        print("1. Přidat film")
        print("2. Zobrazit film")
        print("3. Průměrné hodnocení")
        print("4. Konec")

        choice = input("Vyber akci: ")

        try:
            if choice == "1":
                title = input("Název: ")
                year = input("Rok: ")
                rating = input("Hodnocení (0-10): ")
                manager.add_movie(title, year, rating)

            elif choice == "2":
                title = input("Název filmu: ")
                try:
                    movie = manager.get_movie(title)
                    print(f"{movie['title']} ({movie['year']}) – rating {movie['rating']}")
                except MovieNotFoundError as e:
                    print(e)

            elif choice == "3":
                avg = manager.calculate_average_rating()
                if avg is not None:
                    print(f"Průměrné hodnocení: {avg}")

            elif choice == "4":
                print("Konec programu.")
                break
            else:
                print("Neplatná volba, zkus znovu.")

        except Exception as e:
            print(f"Neošetřená chyba: {e}")
