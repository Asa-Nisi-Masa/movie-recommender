from typing import List, Optional


class Movie:

    __slots__ = (
        "__id_",
        "__imdb_id",
        "__title",
        "__encoding",
        "__genres",
        "__year",
        "__hyperlink",
        "__poster",
    )

    def __init__(
        self,
        id_: str,
        imdb_id: str,
        title: str,
        encoding: Optional[List[float]] = None,
        genres: Optional[str] = None,
        year: Optional[str] = None,
        hyperlink: Optional[str] = None,
        poster: Optional[str] = None,
    ):

        self.__id_ = id_
        self.__imdb_id = imdb_id
        self.__title = title
        self.__encoding = encoding

        self.__genres = genres
        self.__year = year
        self.__hyperlink = hyperlink
        self.__poster = poster

    def __str__(self) -> str:
        return "Movie(id={}, imdb_id={}, title={}".format(
            self.__id_, self.__imdb_id, self.__title,
        )

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def id_(self) -> str:
        return self.__id_

    @property
    def imdb_id(self) -> str:
        return self.__imdb_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def genres(self) -> str:
        return self.__genres

    @property
    def year(self) -> str:
        return self.__year

    @property
    def encoding(self) -> Optional[List[float]]:
        return self.__encoding

    @property
    def hyperlink(self) -> Optional[str]:
        return f"https://www.imdb.com/title/{self.__imdb_id}"

    @property
    def poster(self) -> Optional[str]:
        return self.__poster
