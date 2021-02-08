import unittest

from app import api
from src.services.test_db_manager import test_db_manager
from src.movie_exception import MovieException


class UserRatingsManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_db_manager.setup_test_db()

    @classmethod
    def tearDownClass(cls):
        test_db_manager.teardown_test_db()

    def setUp(self):
        self.__app = api.app.test_client()
        self.__data_valid = (
            "./resources/file_valid.csv",
        )

        self.__data_invalid = (
            ("./resources/file_empty.csv", MovieException.error_empty_file_attached),
            ("./resources/file_missing_imdb_id.csv", MovieException.error_data_frame_missing_key),
            ("./resources/file_missing_ratings.csv", MovieException.error_data_frame_missing_key),
        )

    def test_invalid_files(self):
        for path, expected_error in self.__data_invalid:
            with open(path, "rb") as file:
                response = self.__app.post("/ratings-upload", data={"file": file}).json
                self.assertEqual(response["error"], expected_error)


if __name__ == "__main__":
    unittest.main()
