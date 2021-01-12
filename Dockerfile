FROM postgres:13

RUN apt-get update && \
    apt-get install -y python3 python3-pip sudo cmake make postgresql-server-dev-13

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app/movies
COPY . /app/movies

RUN pip3 install -r requirements.txt --no-cache-dir

WORKDIR /app/movies/postgres_cosine_similarity
RUN make && \
    sudo make install

WORKDIR /app/movies

RUN chmod u+x ./wait-for-it.sh

EXPOSE 5000
ADD init.sh /docker-entrypoint-initdb.d
