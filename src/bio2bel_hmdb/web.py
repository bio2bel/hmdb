# -*- coding: utf-8 -*-


import flask_admin
from flask import Flask
from flask_admin.contrib.sqla import ModelView

from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import *


def add_admin(app, manager):
    admin = flask_admin.Admin(app, url='/')
    admin.add_view(ModelView(Metabolite, manager.session))
    admin.add_view(ModelView(Pathways, manager.session))
    admin.add_view(ModelView(Diseases, manager.session))
    admin.add_view(ModelView(Proteins, manager.session))
    return admin


def create_application(connection=None):
    app = Flask(__name__)
    manager = Manager(connection=connection)
    add_admin(app, manager)
    return app


if __name__ == '__main__':
    app = create_application()
    app.run(debug=True, host='0.0.0.0', port=5000)
