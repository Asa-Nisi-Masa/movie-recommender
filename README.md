
# Movie-recommender


## About The Project

This repository contains the source code for the movie recommender app which can be found at

http://www.movierecommender.org

The app uses a matrix factorization model to learn user and movie embeddings. These embeddings can then be used to find similar movies or to recommend movies to a new user.


## Getting Started

This section contains the steps required to reproduce the app locally. Depending on how closely you want to replicate the app, some steps can possibly be ignored.

### Prerequisites

- docker engine and docker-compose
- postgres service
- python-dotenv (pip3 install python-dotenv==0.15.0)
- yoyo_migrations (pip3 install yoyo_migrations==7.2.0)

### Repository setup
1. Clone the repository

2. Obtain a Movie API key at [http://www.omdbapi.com](http://www.omdbapi.com) (this project uses the poster API)

3. Add the API key to the `.env.example` file and rename the file to `.env`

### Encoding setup

I do not provide the user/movie encodings - you will have to train those by yourself. There are many freely available datasets which can be used.

### Database setup

You will need to generate a database dump with the movie and user encodings, titles and IMDb ids to be used by the app. This database dump will be used by docker during containerization to initialize the (docker) postgres database.

- Make sure the postgres service is running and that a database matching the name in the `.env` file exists.

- Run `python3 migrate.py`

You should now have a database with multiple empty tables. It is up to you to fill the `movies` and `users` tables with the encodings you have trained. You should also fill the `movies` table with the IMDb ids and titles of the movies from your training dataset.

Once the tables have been filled, generate a database dump with, e.g.

`sudo -H -u postgres pg_dump db > db.sql`

## Running

- `docker-compose up`
- Go to `0.0.0.0:5000`
