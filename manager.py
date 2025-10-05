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
            print("File not found. A new one will be created automatically.")
            print("Tip: If you have a backup of your movies.csv, copy it into this folder.")
            self.movies = []
        except PermissionError:
            print("Access denied when trying to read the file.")
            print("Tip: Make sure the file isn't opened by another program (like Excel).")
            self.movies = []
        except Exception as e:
            print(f"Unexpected error while reading from CSV: {e}")
            print("Tip: Check if the file is corrupted or incorrectly formatted as CSV.")

    # Saving CSV
    def save_movies(self):
        try:
            with open(self.filename, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["title", "genre", "year", "rating"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.movies)
        except PermissionError:
            print("Could not save the file – access denied.")
            print("Tip: Make sure the file isn't currently open in another program.")
        except Exception as e:
            print(f"Saving to the file failed: {e}")
            print("Tip: Check your disk space or try saving to a different folder.")

    # Getting rating from OMDb
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
                    "rating": data.get("omdbRating", "N/A"),  # fixed key typo
                    "plot": data.get("Plot", "No description available.")
                }
            else:
                print(f"'{title}' was not found on OMDb.")
                print("Tip: Try typing the exact movie title, for example 'The Matrix' instead of 'Matrix'.")
                return None

        except requests.exceptions.ConnectionError:
            print("Connection to OMDb API failed.")
            print("Tip: Check your internet connection.")
            return None
        except requests.exceptions.Timeout:
            print("The request to OMDb API timed out.")
            print("Tip: Try again in a few seconds.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Communication with API failed: {e}")
            print("Tip: Verify that your API key is valid at https://www.omdbapi.com/apikey.aspx.")
            return None

    # Searching on OMDb
    def search_online(self, title):
        """Will search movie and ask if you want to add the movie to the file."""
        movie = self.fetch_movie_from_api(title)
        if movie:
            print("\n🎬 Movie found:")
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
            print("Movie wasn't found on OMDb.")

    # Adding a movie
    def add_movie(self, title, genre, year, rating=None):
        try:
            year = int(year)
        except ValueError:
            print("Year must be a number (e.g., 1999).")
            print("Tip: Do not include spaces or letters, only digits.")
            return

        if rating is None:
            movie_data = self.fetch_movie_from_api(title)
            rating = movie_data["rating"] if movie_data else "N/A"

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        print(f"'{title}' added to the list (rating: {rating}).")
        self.save_movies()

    # Show all movies in file
    def show_movies(self):
        if not self.movies:
            print("No movies are saved yet.")
            print("Tip: Add one using option 1 in the main menu.")
            return
        print("\n🎞️ Saved movies:")
        for movie in self.movies:
            print(f"- {movie['title']} ({movie['year']}) – {movie['genre']} – OMDb: {movie['rating']}")

    # Searching movies
    def search_movies(self, keyword, field="title"):
        results = [
            m for m in self.movies
            if keyword.lower() in str(m[field]).lower()
        ]
        if results:
            print(f"\nFound movies containing '{keyword}':")
            for movie in results:
                print(f"- {movie['title']} ({movie['year']}) – {movie['genre']} – OMDb: {movie['rating']}")
        else:
            print("No matching movies found.")
            print("Tip: Try a different keyword or check your spelling.")


if __name__ == "__main__":
    manager = MovieManager(api_key="d8ec2719")

    while True:
        print("\nMovie Manager:")
        print("1. Add movie")
        print("2. Show all movies")
        print("3. Search movies by title")
        print("4. Search movies by genre")
        print("5. Search movies by rating")
        print("6. Search movies on OMDb")
        print("7. Exit")

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
            title = input("Enter movie title to search on OMDb: ")
            manager.search_online(title)

        elif choice == "7":
            print("Exiting Movie Manager. See you next time!")
            break

        else:
            print("Invalid choice.")
            print("Tip: Please choose a number between 1 and 7.")

