#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
from typing import Generator
from backup_nas.database import Connector


class Movie:
    def __init__(self, id=None, path=None, size=0, create_time=None, disk_id=None):
        self.id = id
        self.path = Path(path)
        self.size = size
        self.create_time = create_time
        self.disk_id = disk_id

    def __repr__(self) -> str:
        return f"""
            "id": { self.id }
            "path": { self.path }
            "size": { self.size }
            "create_time": { self.create_time }
            "disk_id": { self.disk_id }
        """

    def get_movie_name(self) -> str:
        return self.path.name


class MovieModel:
    def __init__(self, database_name):
        self.connector = Connector(database_name)

    def get_higher_disk_id(self) -> int:
        sql_command = """
        SELECT MAX(disk_id)
        FROM movies
        """
        return self.connector.fetch_one(sql_command)[0]

    def get_movie_size_sum_by_disk_id(self, disk_id: int) -> int:
        sql_command = """
        SELECT SUM(size)
        FROM movies
        WHERE disk_id = ?
        """
        params = (disk_id,)
        return self.connector.fetch_one(sql_command, params)[0] or 0

    def get_movies_by_disk_id(self, disk_id: int) -> list:
        sql_comamnd = """
        SELECT id, path, size, create_time, disk_id
        FROM movies
        WHERE disk_id = ?
        """
        params = (disk_id, )
        return [Movie(*movie) for movie in self.connector.fetch_all(sql_comamnd, params)]

    def insert(self, path: str, size: int, create_time: datetime) -> None:
        sql_command = """REPLACE INTO movies (path, size, create_time)
        VALUES (?, ?, ?)"""
        params = (path, size, create_time)
        self.connector.execute(sql_command, params)

    def fetch_all(self) -> Generator[Movie, None, None]:
        sql_command = """
        SELECT id, path, size, create_time, disk_id
        FROM movies;
        """
        for movie in self.connector.fetch_all(sql_command):
            yield Movie(*movie)

    def fetch_movies_not_disk_tagged(self) -> Generator[Movie, None, None]:
        sql_command = """
        SELECT id, path, size, create_time, disk_id
        FROM movies
        WHERE disk_id IS NULL;
        """
        for movie in self.connector.fetch_all(sql_command):
            yield Movie(*movie)

    def update_movie_with_disk_tag(self, movie_id: int, disk_id: int) -> None:
        sql_command = """
        UPDATE movies
        SET disk_id = ?
        WHERE id = ?
        """
        params = (disk_id, movie_id)
        self.connector.execute(sql_command, params)


def create_movie_database_if_exists(database_name):
    Connector(database_name).execute("""CREATE TABLE if not exists movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL UNIQUE,
        size INT NOT NULL,
        create_time TIMESTAMP NOT NULL,
        disk_id INT DEFAULT NULL);
    """)

