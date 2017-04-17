from flask import Flask


def create_app(package_name, config, extensions=None):
    app = Flask(package_name)
    app.config.from_object(config)
    config.init_app(app)
    
    if extensions:
        for extension in extensions:

            extension.init_app(app)

    return app
