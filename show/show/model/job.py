# -*- coding: utf-8 -*-


from show.model.model import Model


class Job(Model):
    @classmethod
    def init(cls, col):
        cls.col = col
