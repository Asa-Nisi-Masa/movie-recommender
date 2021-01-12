"""
added searched movies
"""

from yoyo import step

__depends__ = {'20201102_01_JfCHW-create-table'}

steps = [
    step(
        "CREATE TABLE searched_movies \
        (\
            id SERIAL,\
            uuid UUID NOT NULL DEFAULT uuid_generate_v1(),\
            user_id VARCHAR(255) NOT NULL,\
            movie_id VARCHAR(255) NOT NULL\
        )",
        "DROP TABLE searched_movies"
    ),
]
