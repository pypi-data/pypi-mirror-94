# XXX
__version__ = "TBD"

import os
from ps.basic import Config

from flask import Flask


def create_app(name, have_config_file=False, test_config=None):
    # create and configure the app
    here = os.path.dirname(os.path.realpath(__file__))
    app = Flask(
        name,
        instance_relative_config=True,
        template_folder=os.path.join(here, "templates"),
    )
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        if app.config["TESTING"]:
            Config.reset_singleton()

    Config.Basic(name, have_config_file=have_config_file)
    app.config["DATABASE"] = Config.herald_sqlite_filename
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True
    from . import database

    database.init_app(app)

    from . import bare_html_api

    app.register_blueprint(bare_html_api.bp)
    app.add_url_rule("/", endpoint="index")

    return app
