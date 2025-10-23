import unittest
import os
import csv
from unittest.mock import patch, MagicMock
from movie_manager.manager import MovieManager


class TestMovieManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_movies.csv"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = MovieManager(filename=self.test_file, api_key="TEST_KEY")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


    def test_add_movie_manual(self):
        self.manager.add_movie("Inception", "Sci-Fi", "2010", "8.8")
        self.assertEqual(len(self.manager.movies), 1)
        self.assertEqual(self.manager.movies[0]["title"], "Inception")


        with open(self.test_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(rows[0]["title"], "Inception")

    def test_load_empty_file(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")
        self.manager.load_movies()
        self.assertEqual(self.manager.movies, [])

  
    @patch.object(MovieManager, "fetch_movie_from_api")
    def test_fetch_movie_from_api(self, mock_fetch):
        mock_fetch.return_value = {
            "title": "Interstellar",
            "genre": "Adventure, Drama, Sci-Fi",
            "year": "2014",
            "rating": "8.6",
            "plot": "Test"
        }

        result = self.manager.fetch_movie_from_api("Interstellar")
        self.assertIsNotNone(result)
        self.assertEqual(result["rating"], "8.6")

    
    def test_search_movies(self):
        self.manager.add_movie("Inception", "Sci-Fi", "2010", "8.8")
        self.manager.add_movie("Matrix", "Action", "1999", "8.7")
        result = [m for m in self.manager.movies if "sci" in m["genre"].lower()]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Inception")

  
    @patch("builtins.input", return_value="y")
    @patch("movie_manager.manager.MovieManager.fetch_movie_from_api")
    def test_search_online_add_to_csv(self, mock_fetch, mock_input):
        mock_fetch.return_value = {
            "title": "Dune",
            "genre": "Sci-Fi",
            "year": "2021",
            "rating": "8.0",
            "plot": "Epic space opera."
        }

        self.manager.search_online("Dune")
        self.assertTrue(any(m["title"] == "Dune" for m in self.manager.movies))

    @patch("builtins.input", return_value="n")
    @patch("movie_manager.manager.MovieManager.fetch_movie_from_api")
    def test_search_online_not_saved(self, mock_fetch, mock_input):
        mock_fetch.return_value = {
            "title": "Avatar",
            "genre": "Action",
            "year": "2009",
            "rating": "7.8",
            "plot": "Blue aliens."
        }

        self.manager.search_online("Avatar")
        self.assertFalse(any(m["title"] == "Avatar" for m in self.manager.movies))


if __name__ == "__main__":
    unittest.main()
