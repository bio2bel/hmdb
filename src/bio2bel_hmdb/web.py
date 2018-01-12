# -*- coding: utf-8 -*-

import flask_admin
from flask import Flask
from flask_admin.contrib.sqla import ModelView

from .manager import Manager
from .models import *


def create_application(connection=None):
    app_ = Flask(__name__)
    manager = Manager(connection=connection)
    add_admin(app_, manager)
    return app


def add_admin(app, session, **kwargs):
    admin = flask_admin.Admin(app, **kwargs)
    admin.add_view(ModelView(Metabolite, session))
    admin.add_view(ModelView(Pathways, session))
    admin.add_view(ModelView(Diseases, session))
    admin.add_view(ModelView(Proteins, session))
    return admin


if __name__ == '__main__':
    app = create_application()
    app.run(debug=True, host='0.0.0.0', port=5000)
