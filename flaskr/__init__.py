import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mmapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    

    @app.route('/hello')
    def hello():
      return 'Hello, World!'

    from . import db
    db.init_app(app)


    from . import bib_photos
    app.register_blueprint(bib_photos.bp)
    app.add_url_rule('/', endpoint='index')

    from . import bib_functions
    # app.register_blueprint(bib_functions.test_bp)


    return app 