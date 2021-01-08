from flask_restx import Namespace

# This is the index of which models are available per user
# api_ns_db = Namespace('models', description='This is the logic that manage the '
#                                             'different model stored in the server')

# This was the namespace for a more RESTful design
# api_ns_geomodels = Namespace('_geomodels',
#                              description='Logic to load and edit the geological model.')

# api_ns_engine = Namespace('engine',
#                           description='End point that handles pretty much all'
#                                       'the business logic necessary for the project')


api_ns_geomodels = Namespace('geomodels',
                             description='This is the logic that manage the ' 
                                         'different model stored in the server.' 
                                         'Also deals with editing.')
