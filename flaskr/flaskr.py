# @Author: Daniel McGlinchey <dan_mac>
# @Date:   2017-06-16T11:43:08-04:00
# @Email:  dmcglinchey2779@icloud.com
# @Filename: flaskr.py
# @Last modified by:   dan_mac
# @Last modified time: 2017-06-16T12:00:59-04:00
#application module
#all the imports
import os
import sqlite3
from flask import Flask, request,session, g, redirect, url_for, abort, \
    render_template, flash

#create the application instance
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode = 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database"""
    init_db()
    print('Initialized the database')

def get_db():

    """ Opens a new database connection if there is none yet for the current
    application context
    """
    if not hasattr(g, 'sqlite_db'):
        g.squlite_db = connect_db()
    return g.squlite_db

@app.teardown_appcontext
def close_db(error):
    """ Close the database again at the end of the request"""

    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
