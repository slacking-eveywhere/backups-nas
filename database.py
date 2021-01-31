#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3


class Connector:
    def __init__(self, database_name):
        self.database_name = database_name

    def execute(self, sql_command, params=()):
        with sqlite3.connect(self.database_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_command, params)
            conn.commit()

    def fetch_one(self, sql_command, param=()):
        with sqlite3.connect(self.database_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_command, param)
            return cursor.fetchone()

    def fetch_all(self, sql_command, param=()):
        with sqlite3.connect(self.database_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_command, param)
            return cursor.fetchall()