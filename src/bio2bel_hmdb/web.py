# -*- coding: utf-8 -*-

"""This module builds a :mod:`Flask` application for interacting with the underlying database. When installing,
use the web extra like:

.. source-code:: sh

    pip install bio2bel_hmdb[web]
"""

import flask_admin
from flask import Flask
from flask_admin.contrib.sqla import ModelView

from .manager import Manager
from .models import *


def add_admin(app, session, **kwargs):
    """Adds a Flask Admin interface to an application

    :param flask.Flask app:
    :param session:
    :param kwargs:
    :rtype: flask_admin.Admin
    """
    admin = flask_admin.Admin(app, **kwargs)

    admin.add_view(ModelView(Metabolite, session))
    admin.add_view(ModelView(Pathways, session))
    admin.add_view(ModelView(Diseases, session))
    admin.add_view(ModelView(Proteins, session))

    return admin


def get_app(connection=None, url=None):
    """Creates a Flask application

    :type connection: Optional[str or bio2bel_hmdb.Manager]
    :type url: Optional[str]
    :rtype: flask.Flask
    """
    app = Flask(__name__)
    manager = Manager.ensure(connection=connection)
    add_admin(app_, manager, url=url)
    return app


if __name__ == '__main__':
    app_ = get_app()
    app_.run(debug=True, host='0.0.0.0', port=5000)
