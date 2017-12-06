# -*- coding: utf-8 -*-


from show import mongo


class Job(object):
    col = 'lagou'
    cond = {}

    @classmethod
    def set(cls, cond):
        cls.cond = cond

    @classmethod
    def find(cls):
        return mongo.db[cls.col].find(cls.cond)
