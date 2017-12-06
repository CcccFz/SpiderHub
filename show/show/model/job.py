# -*- coding: utf-8 -*-


from show import mongo


class Job(object):
    col = 'lagou'

    def __init__(self, col):
        self.col = col

    @classmethod
    def count(cls):
        return mongo.db[cls.col].count()

    @classmethod
    def find(cls, **kwargs):
        return mongo.db[cls.col].find(kwargs)
