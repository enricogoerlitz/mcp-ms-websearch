from flask import Flask
from flask_cors import CORS

from apis.v1.health import bp as bp_health_v1
from apis.v1.mcp import bp as bp_mcp_v1


class FlaskConfig:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "https://yourfrontend.com"}})

    app.register_blueprint(bp_health_v1)
    app.register_blueprint(bp_mcp_v1)

    return app
