import unittest
import os
import json
from movie_manager.main import MovieManager, MovieNotFoundError


class TestMovie(unittest.TestCase):
    def setUp(self):
        # Create a test file
        self.test_file = "test_movies.json"
        # If the test file already exists, we will remove it and replace it with new one
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = MovieManager(filename=self.test_file)

    def tearDown(self):
        # After the test we remove the test file, so it wont confuse us
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_movie(self):
        # Test if the function runs successfully
        self.manager.add_movie("Inception", 2010, 9.0)
        self.assertEqual(len(self.manager.movies), 1)
        self.assertEqual(self.manager.movies[0]["title"], "Inception")
        self.assertEqual(self.manager.movies[0]["rating"], 9.0)

    def test_calculate_average_rating(self):
        self.manager.add_movie("Movie 1", 2015, 7.0)
        self.manager.add_movie("Movie 2", 2003, 5.0)
        avg = self.manager.calculate_average_rating()
        self.assertEqual(avg, 6.0)

    def test_movie_not_found(self):
        with self.assertRaises(MovieNotFoundError):
            self.manager.get_movie("Movie doesnt exist")

if __name__ == '__main__':
    unittest.main()