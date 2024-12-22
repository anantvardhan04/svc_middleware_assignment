from flask import Flask, request
from app.extensions import db
from app.config import Config


def create_ap(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize flask extensions
    db.init_app(app)

    # Register blueprints
    from app.account_core import bp as account_bp

    app.register_blueprint(account_bp, url_prefix="/account")

    return app
