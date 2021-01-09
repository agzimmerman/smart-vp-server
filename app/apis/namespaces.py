from flask_restx import Namespace

# This is the index of which models are available per user

api_ns_geomodels = Namespace('geomodels',
                             description='This is the logic that manage the ' 
                                         'different model stored in the server.' 
                                         'Also deals with editing.')

api_ns_smart_vp = Namespace('smartvp',
                            description='App for vp challenge phase 1');