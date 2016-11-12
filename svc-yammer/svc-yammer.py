# -*- coding: utf-8 -*-

from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from cassandra.cluster import Cluster
from prometheus_client import Counter, ProcessCollector

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SVC_YAMMER_SETTINGS', silent=True)


# configuration
CASSANDRA_IP = '127.0.0.1'
CASSANDRA_PORT = '9042'
YAMMER_KEYSPACE = 'yammer'


ProcessCollector(namespace='svc-yammer', pid=lambda: open('/var/run/daemon.pid').read()).collect()


@app.route('/')
def hello():
    return 'Hello'


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'cassandra_db'):
        top.cassandra_db.close()


@app.before_request
def before_request():
    """Execute before each request"""
    True


def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    top = _app_ctx_stack.top
    if not hasattr(top, 'cassandra_db'):
        top.cassandra_db = Cluster([app.config['DATABASE_IP']], port=app.config['CASSANDRA_PORT'])\
                            .connect(app.config['YAMMER_KEYSPACE'])
    return top.cassandra_db


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    True


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url

app.run(port=8000)

