#
# Flask-Turbo
#
# Copyright (C) 2021 Boris Raicheff
# All rights reserved
#


import logging


logger = logging.getLogger('Flask-Turbo')


class Turbo(object):
    """
    Flask-Turbo

    https://pypi.python.org/pypi/flask-turbo

    https://flask-turbo.readthedocs.io

    :param app: Flask app to initialize with. Defaults to `None`
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['turbo'] = self


# EOF
