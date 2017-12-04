# -*- coding: utf-8 -*-


from flask import request, render_template, flash, abort, url_for, redirect, session, Response
from show import app


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')
