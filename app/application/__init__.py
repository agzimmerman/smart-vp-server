from flask import Flask
from flask_cors import CORS
from app.application.geomodels import routes as gm_routes
from app.apis import api


def create_app():
    """Initialize the core application"""
    app = Flask(__name__)
    
    CORS(app)
    
    api.init_app(app)

    # app.config['SERVER_NAME'] = 'gempyserver'

    # Set flask configuration
    # app.config.from_object('config.Config')

    # In case down the line we want to add blueprints
    # with app.app_context():
    #     swagger_doc = json.dumps(api.__schema__,  sort_keys=True, indent=4)
    #     with open('swagger_doc3.json', 'w') as f:
    #         f.seek(0)
    #         json.dump(swagger_doc, f, indent=4, sort_keys=True)
    #         f.truncate()
    #     # Register blueprints
    #     app.register_blueprint(routes.models_bp)

    return app
