#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
from pathlib import Path, PureWindowsPath
from datetime import datetime
from typing import Generator
from movie_model import MovieModel
from disks import Disks

MOVIE_PATH = Path("/Volumes/medias/films")
BAT_PATH = Path("/Volumes/medias/divers/bk")


def insert_movies(cont=False) -> None:
    if cont is False:
        return

    movie_paths = (movie_path for movie_path in MOVIE_PATH.iterdir())

    for movie_path in movie_paths:
        size = sum(f.stat().st_size for f in movie_path.glob('**/*') if f.is_file())
        create_time = movie_path.stat().st_ctime
        MovieModel().insert(str(movie_path), size, datetime.fromtimestamp(create_time))


def accumulate_movies_by_size(movies: Generator, disks_list: Disks) -> None:
    disk_id = MovieModel().get_higher_disk_id() or 1

    while True:
        try:
            movie = next(movies)
            limit = disks_list.get_disk_by_index(disk_id).size
            if MovieModel().get_movie_size_sum_by_disk_id(disk_id) + movie.size >= limit:
                disk_id = MovieModel().get_higher_disk_id() + 1
            MovieModel().update_movie_with_disk_tag(movie.id, disk_id)

        except StopIteration:
            break


if __name__ == "__main__":
    insert_movies()

    disks = Disks().load()

    accumulate_movies_by_size(
        MovieModel().fetch_movies_not_disk_tagged(),
        disks
    )

    # for i in range(1,len(disks) + 1):
    #     print(MovieModel().get_movie_size_sum_by_disk_id(i) / pow(1024, 4))

