#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from pathlib import Path
from datetime import datetime
from backup_nas.movie_model import MovieModel, create_movie_database_if_exists
from backup_nas.disks import Disks


INSERT_MOVIE = False
MOVIES_DIRECTORY_PATH = Path("/data-dir/films")
DATABASE_NAME = "database.sql"
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

    create_movie_database_if_exists(DATABASE_NAME)

    movie_model = MovieModel(DATABASE_NAME)
    disks_list = Disks()

    # for movie_path, movie_size, movie_insert_date in list_movies_with_name_size_and_insert_date(MOVIES_DIRECTORY_PATH):
    #     movie_model.insert(movie_path, movie_size, movie_insert_date)

    disk_id = movie_model.get_higher_disk_id() or 1

    for movie in movie_model.fetch_movies_not_disk_tagged():
        limit = disks_list.get_disk_by_index(disk_id).size
        if movie_model.get_movie_size_sum_by_disk_id(disk_id) + movie.size >= limit:
            disk_id = movie_model.get_higher_disk_id() + 1
        movie_model.update_movie_with_disk_tag(movie.id, disk_id)

    print(humanize_size_output_from_bytes(movie_model.get_movie_size_sum_by_disk_id(14)))

