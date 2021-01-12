class MovieException(Exception):

    error_no_movie_found_by_title = "no_movie_found_by_title"
    error_data_frame_missing_key = "data_frame_missing_key"
    error_empty_file_attached = "empty_file_attached"

    def __init__(self, code: str, message: str):
        super(MovieException, self).__init__(message)
        self.__code = code

    @property
    def code(self) -> str:
        return self.__code
