# -*- coding: utf-8 -*-


import flask_admin
from flask import Flask
from flask_admin.contrib.sqla import ModelView

from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import *


def add_admin(app, session, url=None):
    admin = flask_admin.Admin(app, url=(url or '/'))
    admin.add_view(ModelView(Metabolite, session))
    admin.add_view(ModelView(Pathways, session))
    admin.add_view(ModelView(Diseases, session))
    admin.add_view(ModelView(Proteins, session))
    return admin


def create_app(connection=None, url=None):
    """Creates a Flask application

    :type connection: Optional[str]
    :rtype: flask.Flask
    """
    app = Flask(__name__)
    manager = Manager(connection=connection)
    add_admin(app, manager.session, url=url)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
