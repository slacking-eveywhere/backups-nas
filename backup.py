#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import re
import math
from tasks import Task

DIR_PATH = "/Volumes/media/series"

FILE_SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]


class Disk:
    def __init__(self):
        self._contents = []

    def __iter__(self):
        return iter(self._contents)

    def add_content(self, content):
        self._contents.append(content)
        return self

    def dumps(self):
        return [{"path": str(content), "size": content.get_content_size_in_bytes()} for content in self]


class DisksDatastructure:
    def __init__(self):
        self._disks = [Disk()]

    def __iter__(self):
        return iter(self._disks)

    def add_new_disk(self):
        self._disks.append(Disk())
        return self

    def get_last_disk(self):
        return self._disks[len(self._disks) - 1]

    def dumps(self):
        return [{"disk": disk.dumps()} for disk in self]


class Contents:
    def __init__(self, root_dir, disk_size):
        self.root_dir = root_dir
        self.disk_size = computize_size_input_in_bytes(disk_size)

    def __iter__(self):
        try:
            for content in sorted(os.listdir(self.root_dir)):
                content_path = Path(os.path.join(self.root_dir, content))
                if content_path.name.startswith(".") is False:
                    yield Content(content_path)

        except FileNotFoundError:
            print(f"No file here { self.root_dir }")

    def fit_in(self):
        batched_content_size = 0
        disks = DisksDatastructure()

        for content in self:
            content_size = content.get_content_size_in_bytes()
            if batched_content_size + content_size < self.disk_size:
                batched_content_size += content_size
            else:
                disks.add_new_disk()
                batched_content_size = content_size

            disks.get_last_disk().add_content(content)

        return disks


class Content:
    def __init__(self, path):
        self.path = path
        self._size = None

    def __repr__(self):
        return self.path.name

    def __str__(self):
        return str(self.path)

    def get_parent(self):
        return self.path.parent

    def get_content_size_in_bytes(self):
        if not self._size:
            self._size = sum(f.stat().st_size for f in self.path.glob("**/*"))

        return self._size


def humanize_size_output_from_bytes(size_in_bytes):
    unit_index = int(math.floor(math.log(size_in_bytes, 1024)))
    current_size = size_in_bytes / math.pow(1024, unit_index)
    return f"{ round(current_size, 2) } { FILE_SIZE_UNITS[unit_index] }"


def computize_size_input_in_bytes(size_as_string):
    a = re.search("([. 0-9]*)(B|KB|MB|GB|TB)", size_as_string)
    if a:
        value, unit = a.groups()
        unit_index = FILE_SIZE_UNITS.index(unit)
        return int(int(value) * math.pow(1024, unit_index))


if __name__ == "__main__":
    series = Task('series', DIR_PATH, "2TB")
    # contents = Contents(DIR_PATH, "2TB")
    # series.set_distribution(contents.fit_in())
    # series.save()
    print(series.load())

