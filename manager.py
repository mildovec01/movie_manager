import csv
import requests


class MovieManager:
    def __init__(self, filename="movies.csv", api_key="d8ec2719"):
        self.filename = filename
        self.api_key = api_key
        self.movies = []
        self.load_movies()

    # Load CSV
    def load_movies(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.movies = list(reader)
        except FileNotFoundError:
            print("File doesn't exist, creating a new one.")
            self.movies = []
        except Exception as e:
            print(f"Reading from CSV failed: {e}")

    # Saving CSV
    def save_movies(self):
        try:
            with open(self.filename, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["title", "genre", "year", "rating"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.movies)
        except Exception as e:
            print(f"Saving to the file failed: {e}")

    # Getting rating from OMBd
    def fetch_movie_from_api(self, title):
        try:
            url = f"https://www.omdbapi.com/?t={title}&apikey={self.api_key}&plot=short"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "True":
                return {
                    "title": data.get("Title", "Unknown"),
                    "genre": data.get("Genre", "Unknown"),
                    "year": data.get("Year", "Unknown"),
                    "rating": data.get("omdbRating", "N/A"),
                    "plot": data.get("Plot", "No description available.")
                }
            else:
                print(f"'{title}' wasnt found on OMDb.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Communication with API failed: {e}")
            return None

    # Searching on OMDb
    def search_online(self, title):
        """Will search movie and ask if you want to add the movie to the file."""
        movie = self.fetch_movie_from_api(title)
        if movie:
            print("\nMovie found:")
            print(f"  Title: {movie['title']}")
            print(f"  Year: {movie['year']}")
            print(f"  Genre: {movie['genre']}")
            print(f"  OMDb rating: {movie['rating']}")
            print(f"  Description: {movie['plot']}")

            choice = input("\nDo you want to add the movie to the file? (y/n): ").strip().lower()
            if choice == "y":
                self.movies.append({
                    "title": movie["title"],
                    "genre": movie["genre"],
                    "year": movie["year"],
                    "rating": movie["rating"]
                })
                self.save_movies()
                print(f"'{movie['title']}' was added to the file.")
            else:
                print("Movie wasn't saved.")
        else:
            print("Movie wasn't found.")

    # Adding a movie
    def add_movie(self, title, genre, year):
        try:
            year = int(year)
        except ValueError:
            print("Year has to be a number.")
            return

        rating = self.fetch_movie_from_api(title)

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        print(f"'{title}' added to the list.")
        self.save_movies()

    # Show all movies in file
    def show_movies(self):
        if not self.movies:
            print("No movies are saved.")
            return
        print("\nSaved movies:")
        for movie in self.movies:
            print(f"- {movie['title']} ({movie['year']}) – {movie['genre']} – OMDb: {movie['rating']}")

    # Searching movies
    def search_movies(self, keyword, field="title"):
        results = [
            m for m in self.movies
            if keyword.lower() in str(m[field]).lower()
        ]
        if results:
            print(f"\nFound movies '{keyword}':")
            for movie in results:
                print(f"- {movie['title']} ({movie['year']}) – {movie['genre']} – OMDb: {movie['rating']}")
        else:
            print("No movies found.")


if __name__ == "__main__":
    manager = MovieManager(api_key="d8ec2719")


    while True:
        print("\nMovie Manager:")
        print("1. Add movie")
        print("2. Show all movies")
        print("3. Search movies with title")
        print("4. Search movies with genre")
        print("5. Search movies with rating")
        print("6. Search movies on OMDb")
        print("7. End")

        choice = input("Choose action: ")

        if choice == "1":
            title = input("Movie title: ")
            genre = input("Genre: ")
            year = input("Year: ")
            manager.add_movie(title, genre, year)

        elif choice == "2":
            manager.show_movies()

        elif choice == "3":
            keyword = input("Enter movie title: ")
            manager.search_movies(keyword, field="title")

        elif choice == "4":
            keyword = input("Enter genre: ")
            manager.search_movies(keyword, field="genre")

        elif choice == "5":
            keyword = input("Enter rating (0-10): ")
            manager.search_movies(keyword, field="rating")

        elif choice == "6":
            title = input("Enter movie title: ")
            manager.search_online(title)

        elif choice == "7":
            print("End of the program. Bye.")
            break

        else:
            print("Wrong choice, try again please.")
