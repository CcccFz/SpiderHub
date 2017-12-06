# -*- coding: utf-8 -*-

from flask import render_template, flash, abort, url_for, redirect, session, Response

from show import app
from show.model.job import Job


SALARY = ''
ADVANTAGE = []
PAGE = 10
JOBS = []


@app.route('/', methods=['GET'])
@app.route('/<int:page>', methods=['GET'])
def index(page=None):
    page = page if page else 1
    if SALARY or ADVANTAGE:
        jobs = JOBS[PAGE*(page-1):PAGE*page]
    else:
        jobs = Job.find()[PAGE*(page-1):PAGE*page]
    return render_template('index.html', jobs=jobs, total=len([x for x in jobs]), page=page)


@app.route('/salary/<salary>', methods=['GET'])
def salary(salary=''):
    jobs = []
    check = lambda a, b, x, y: (x <= a and y >= b) or (x >= a and y <= b)

    if salary == u'5k及以下':
        min, max = 0, 5
    elif salary == u'26k以上':
        min, max = 26, 100
    else:
        min, max = salary.split('~')
        max = int(max[:-1])

    for job in Job.find():
        each_min, each_max = job['salary'].split('-')
        each_min = int(each_min[:-1])
        each_max = int(each_max[:-1])
        if check(min, max, each_min, each_max):
            jobs.append(job)

    global JOBS, SALARY
    JOBS = jobs
    SALARY = salary
    return render_template('index.html', jobs=jobs, total=len(jobs))