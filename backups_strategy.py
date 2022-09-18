#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import math
from datetime import datetime
from typing import Generator
from movie_model import MovieModel
from disks import Disks


INSERT_MOVIE = False
MOVIES_DIRECTORY_PATH = Path("/data-dir/films")

FILE_SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]


def list_movies_with_name_size_and_insert_date(movies_directory_path) -> iter:
    movie_paths = (movie_path for movie_path in movies_directory_path.iterdir())

    for movie_path in movie_paths:
        size = sum(file.stat().st_size for file in movie_path.glob('**/*') if file.is_file())
        create_time = movie_path.stat().st_ctime
        yield str(movie_path), size, datetime.fromtimestamp(create_time)


def humanize_size_output_from_bytes(size_in_bytes):
    unit_index = int(math.floor(math.log(size_in_bytes, 1024)))
    current_size = size_in_bytes / math.pow(1024, unit_index)
    return f"{ round(current_size, 2) } { FILE_SIZE_UNITS[unit_index] }"


if __name__ == "__main__":

    if INSERT_MOVIE:
        for movie_path, movie_size, movie_insert_date in list_movies_with_name_size_and_insert_date(MOVIES_DIRECTORY_PATH):
            MovieModel().insert(movie_path, movie_size, movie_insert_date)


    disks_list = Disks().load()
    disk_id = MovieModel().get_higher_disk_id() or 1
    movies = MovieModel().fetch_movies_not_disk_tagged()

    for movie in movies:
        limit = disks_list.get_disk_by_index(disk_id).size
        if MovieModel().get_movie_size_sum_by_disk_id(disk_id) + movie.size >= limit:
            disk_id = MovieModel().get_higher_disk_id() + 1
        MovieModel().update_movie_with_disk_tag(movie.id, disk_id)

    print(humanize_size_output_from_bytes(MovieModel().get_movie_size_sum_by_disk_id(14)))

