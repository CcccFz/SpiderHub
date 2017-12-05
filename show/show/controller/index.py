# -*- coding: utf-8 -*-


from flask import request, render_template, flash, abort, url_for, redirect, session, Response

from show import app
from show.model.job import Job


@app.route('/', methods = ['GET'])
def index():
    Job.init('lagou')
    return render_template('index.html', jobs=Job.all(), total=Job.count())
