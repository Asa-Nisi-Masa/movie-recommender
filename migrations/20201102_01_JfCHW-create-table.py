"""
create_table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE movies \
        (\
            id SERIAL,\
            imdb_id VARCHAR(255) NOT NULL,\
            title VARCHAR(255) NOT NULL,\
            encoding FLOAT4[32]\
        )",
        "DROP TABLE movies"
    ),
    step("CREATE TABLE users \
        (\
            id SERIAL,\
            encoding FLOAT4[32]\
        )",
        "DROP TABLE users"
    ),
]
