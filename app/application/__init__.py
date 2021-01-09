from flask import Flask
from flask_cors import CORS
from app.application.geomodels import routes as gm_routes
from app.application.smart_vp import routes as sm_routes
from app.apis import api


def create_app():
    """Initialize the core application"""
    app = Flask(__name__)
    
    CORS(app)
    
    api.init_app(app)

    print(app.url_map)

    return app
