import os
from flask import Flask
from flask import render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return('Hello, world!')

    from . import overview
    app.register_blueprint(overview.bp)
    app.add_url_rule('/', endpoint='index')

    from . import singlevariable
    app.register_blueprint(singlevariable.bp)
    app.add_url_rule('/singlevariable', endpoint='index')

    @app.route('/about')
    def about():
        return render_template('about/index.html', settings_visible=False)

    return app
	
if __name__ == "__main__":
    app = create_app()
    app.run()