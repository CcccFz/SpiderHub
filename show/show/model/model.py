# -*- coding: utf-8 -*-


from show import mongo


class Model(object):
    col = None

    @classmethod
    def all(cls):
        return mongo.db[cls.col].find()

    @classmethod
    def count(cls):
        return mongo.db[cls.col].count()

    @classmethod
    def get(cls, **kwargs):
        return mongo.db[cls.col].find(kwargs)

    @classmethod
    def filter(cls, **kwargs):
        return mongo.db[cls.col].find(kwargs)

