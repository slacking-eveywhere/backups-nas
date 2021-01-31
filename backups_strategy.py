#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
from movie_model import MovieModel

MOVIE_PATH = Path("/Volumes/medias/films")


def insert_movies(cont=False):
    if cont is False:
        return

    movie_paths = (movie_path for movie_path in MOVIE_PATH.iterdir() if movie_path.name.startswith('A'))

    for movie_path in movie_paths:
        size = sum(f.stat().st_size for f in movie_path.glob('**/*') if f.is_file())
        create_time = movie_path.stat().st_ctime
        MovieModel().insert(str(movie_path), size, datetime.fromtimestamp(create_time))


def accumulate_movies_by_size(movies):
    limit = 200 * pow(1000, 3)
    disk = []

    ms = iter(movies)
    new_list = []

    for movie in movies:
        if sum(m.size for m in disk) + movie.size < limit:
            disk.append(movie)
        else:
            new_list.append(movie)

    return


if __name__ == "__main__":
    insert_movies(False)

    movies = MovieModel().fetch_all()
    print(list(movies))

