#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from database import Connector

DATABASE_NAME = "database.sql"


class Movie:
    def __init__(self, id=None, path=None, size=0, create_time=None):
        self.id = id
        self.path = path
        self.size = size
        self.create_time = create_time


class MovieModel:
    def __init__(self, movie=None):
        self.connector = Connector(DATABASE_NAME)

    def insert(self, path, size, create_time):
        sql_command = """REPLACE INTO movies (path, size, create_time)
        VALUES (?, ?, ?)"""
        params = (path, size, create_time)
        return self.connector.execute(sql_command, params)

    def fetch_all(self):
        sql_command = """
        SELECT id, path, size, create_time
        FROM movies;
        """
        for movie in self.connector.fetch_all(sql_command):
            yield Movie(*movie)


Connector(DATABASE_NAME).execute("""CREATE TABLE if not exists movies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL UNIQUE,
    size INT NOT NULL,
    create_time TIMESTAMP NOT NULL);
""")

