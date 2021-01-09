from flask_restx import Api
from .namespaces import *

api = Api(
    title='GemPy Server',
    version='0.1',
    description='Pre-alpha version of the library which control GemPy as a'
                'service.',
    # All API metadatas
)

api.add_namespace(api_ns_geomodels)
api.add_namespace(api_ns_smart_vp)

