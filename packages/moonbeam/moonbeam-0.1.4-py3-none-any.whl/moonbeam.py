# -*- coding: utf-8 -*-

import os

EXTENSION = ".mb"


class Load:
    def __init__(self, path="main", directory="./", default=None):
        if default is None:
            default = {}

        self.directory = directory
        self.default = default
        self.path = path

        try:
            self.file = open(f"""{self.directory}{self.path}{EXTENSION}""", encoding="utf-8").read()
        except FileNotFoundError:
            open(f"""{self.directory}{self.path}{EXTENSION}""", "w", encoding="utf-8").write(
                f"{self.dumps(self.default)}"
            )
            self.file = open(f"""{self.directory}{self.path}{EXTENSION}""", encoding="utf-8").read()

        self.database = self.loads(self.file)

    def get(self, name, key=None):
        if key is None:
            return self.database[name]
        else:
            return self.database[name][key]

    def set(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]] = value
            self.save()
        else:
            self.database[key] = value
            self.save()

    def append(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]].append(value)
            self.save()
        else:
            self.database[key].append(value)
            self.save()

    def remove(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]].remove(value)
            self.save()
        else:
            self.database[key].remove(value)
            self.save()

    def plus(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]] += value
            self.save()
        else:
            self.database[key] += value
            self.save()

    def minus(self, key, value):
        if type(key) == list:
            self.database[key[0]][key[1]] -= value
            self.save()
        else:
            self.database[key] -= value
            self.save()

    def delete(self, key):
        if type(key) == list:
            del self.database[key[0]][key[1]]
            self.save()
        else:    
            del self.database[key]
            self.save()

    def save(self):
        open(f"""{self.directory}{self.path}{EXTENSION}""", "w", encoding="utf-8").write(f"{self.dumps(self.database)}")

    @staticmethod
    def loads(file):
        result = {}
        for i in file.splitlines():
            obj = i.split(" | ")
            if obj[2] == "int" or obj[2] == "str":
                result[obj[0]] = eval(f"{obj[2]}(obj[1])")
            else:
                result[obj[0]] = eval(obj[1])
        return result

    @staticmethod
    def dumps(obj):
        result = ""
        for name in obj:
            result += f"""{name} | {obj[name]} | {type(obj[name]).__name__}\n"""
        return result


class LoadAll:
    def __init__(self, directory="./"):
        if directory is None:
            self.directory = "./"
        else:
            self.directory = directory

        self.all = [i.replace(EXTENSION, "") for i in os.listdir(self.directory) if i.find(EXTENSION) > 0]
        self.files = {}

        for name in self.all:
            self.files[name] = Load(path=name, directory=self.directory)

    def append(self, name, file):
        self.files[name] = file

    def get(self, name):
        return self.files[name]
