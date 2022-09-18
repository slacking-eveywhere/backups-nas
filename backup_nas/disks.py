#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

DISKS_FILE = "disks_list.yml"
DISK_SIZE_UNIT_LIST = ["o", "ko", "mo", "go", "to"]


class Disks:
    def __init__(self):
        with open(DISKS_FILE, 'r') as stream:
            try:
                self.disks = [Disk(index, **disk) for index, disk in enumerate(yaml.safe_load(stream).get("movies_disks"), start=1)]
            except yaml.YAMLError as exc:
                self.disks = []

    def __len__(self) -> int:
        return len(self.disks)

    def __iter__(self) -> iter:
        for disk in self.disks:
            yield disk

    def get_disk_by_index(self, disk_index: int) -> 'Disk':
        try:
            return next(disk for disk in self if disk.index == disk_index)
        except:
            return None


class Disk:
    def __init__(self, index, name: str, size: int, unit: str):
        self.index = index
        self.name = name
        self.size = convert_size_in_bytes(size, unit)

    def __repr__(self):
        return f"{ self.index } - { self.name } - { self.size }"


def convert_size_in_bytes(size: int, unit: str) -> int:
    return size * pow(1024, DISK_SIZE_UNIT_LIST.index(unit.lower()))
