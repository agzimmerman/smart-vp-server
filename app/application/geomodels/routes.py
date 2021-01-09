# Rest libraries
from flask import json, request, Response
from app.apis.namespaces import api_ns_geomodels
from flask_restx import Resource
from marshmallow import ValidationError
from marshmallow_jsonschema import JSONSchema

# Additional libraries

# Importing modules
from .schemas import ModelsSchema, ModelSchemeDelete, OperationSchema
from ...logic.func_api import OperationController, db

# Defining models

# Init the JSON schema
models_schema_input = ModelsSchema()
model_schema_del = ModelSchemeDelete()

# Create a doc for SWAGGER from the schema
models_schema_input_doc = api_ns_geomodels.schema_model(
    'models_schema_input_doc',
    JSONSchema().dump(
        models_schema_input)['definitions'][
        'ModelsSchema'])


# Business logic classes
operation_controller = OperationController()

# TODO operations has to be a dictionary with keys: operationUrn!
operation_status = dict() # running or finished

op_schema = OperationSchema()
op_schema_doc = api_ns_geomodels.schema_model(
    'models_operations_schema_doc',
    JSONSchema().dump(
        op_schema)['definitions'][
        'OperationSchema'])


@api_ns_geomodels.route('/')
class GeoModelsIndexView(Resource):
    @api_ns_geomodels.doc()
    def get(self):
        """Returns a list of all geomodel available for loading"""
        return db.df.to_dict(orient='index')

    @api_ns_geomodels.doc(body=models_schema_input_doc,
                          responses={201: 'Created. Returning pandas df, orient=\'index\''})
    def post(self, verbose=False):
        """Add a new geomodel entry to the index table"""

        json_data = request.get_json()

        # Check if json is passed
        if not json_data:
            return {"message": "No input data provided"}, 400

        # Here we validate the schema!
        try:
            data = models_schema_input.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        if verbose is True:
            print('data', data)
            print('Requests', request, request.values, request.values.to_dict())

        # Do logic
        db.add_entry(**data)

        if verbose is True:
            print('Pandas to json: ', db.df.to_json())

        return db.df.to_dict(orient='index'), 201


@api_ns_geomodels.route('/<string:geoModelUrn>')
class GeoModelView(Resource):

    def get(self, geoModelUrn):
        """Get some metadata from the model. So far nothing it is the same as
        GET: /geomodels/ """
        return db.df.loc[geoModelUrn].to_json(orient='index'), 201

    def delete(self, geoModelUrn):
        """Delete geomodel"""

        db.delete_entry(geoModelUrn)
        return db.df.to_json(orient='index'), 200

# --- Unused in the server
# @api_ns_geomodels.route('/<string:geoModelUrn>/operations')
# class GeoModelsOperationsView(Resource):
#     @api_ns_geomodels.doc(body=op_schema_doc,
#                           responses={202: 'Operation Urn'})
#     def post(self, geoModelUrn):
#         """Applies an operation. All the model manipulation happen here.
#         body is a json
#
#         :returns
#             Operation Urn
#         """
#         # Parsing json and validating
#         json_data = request.get_json()
#         print(json_data)
#         # Check body exist
#         if not json_data:
#             return {"message": "No input data provided"}, 400
#
#         # Check format of the body
#         try:
#             json_data = op_schema.load(json_data)
#         except ValidationError as err:
#             return err.messages, 422
#
#         operation_status[json_data['op_urn']] = 'running'
#
#         # Need a parser function: That decide what to do with each operation
#         try:
#             operation_controller.parse(**json_data)
#         except Exception as err:
#             return {'Error raised during processing: ': err}, 400
#
#         operation_status[json_data['op_urn']] = 'finished'
#         print(json_data['op_urn'])
#         # Probably I can pass back the operation urn without having the deserialize it
#         return {'Operation Urn': json_data['op_urn']}, 202
#
#
# @api_ns_geomodels.route('/<string:geoModelUrn>/operations/<string:opUrn>/status')
# class GeoModelsStatusView(Resource):
#     @api_ns_geomodels.doc(body=op_schema_doc,
#                           responses={200: 'Operation Urn Status: running | finished'})
#     def get(self, geoModelUrn, opUrn):
#         """Returns the status of the last operation.
#         This could be also reduced to /<string:modelUrn>/operations/<string:opUrn>/ but
#         I can envision other actions - e.g. cancel - to be aplied to an operation
#         """
#         return {'OpStatus': operation_status[opUrn]}
#
#
# @api_ns_geomodels.route('/<string:geoModelUrn>/output')
# class GeoModelsOutputView(Resource):
#     @api_ns_geomodels.doc(body=None, # TODO add schema to filte data
#                           responses={200: 'Rexfile - binary'})
#     def get(self, geoModelUrn):
#         """Get the rexfile with the computed geological model. With a payload (to be defined) we
#         can filter how much data we return, by default output mesh"""
#
#         # TODO Adding the filtering of data using a payload
#         # Parsing json and validating
#
#         # json_data = request.get_json()
#         # print(json_data)
#         # # Check body exist
#         # if not json_data:
#         #     return {"message": "No input data provided"}, 400
#
#         try:
#             # TODO: At some point I am going to need a similar wrapper as OperationsController
#             #  Maybe I/OController or something like that
#             # Rexfile per surface: rex_bytes = gp.geomodel_to_rex(operation_controller.geo_models_dict[geoModelUrn])
#             rex_bytes = gempy_controller.encode_rex(geoModelUrn)
#         # Error: model not loaded
#         except KeyError as err:
#             return {'message': 'No model is loaded yet. Use /operations - to load a model'
#                                ' first: ' + str(err)}, 428
#
#         # except KeyError as err:
#         #     return {'message': 'Model not found. Have you loaded first' + str(err)}, 428
#         #
#         # I think this is model not computed
#         except RuntimeError as err:
#             return err, 428
#
#         # Rexfile per surface: rpn = list(rex_bytes.values())[0]
#         rpn = Response(rex_bytes, status=200)
#         rpn.headers['geo_modelUrn'] = db.df.loc[geoModelUrn, 'm_state']
#
#         return rpn
#
#
# @api_ns_geomodels.route('/<string:geoModelUrn>/input')
# class GeoModelsInputView(Resource):
#     @api_ns_geomodels.doc(body=None,  # TODO add schema to filte data
#                           responses={200: 'json'})
#     def get(self, geoModelUrn):
#         """Get gempy input data in json. With a payload (to be defined) we can
#         filter how much data is sent"""
#
#         # TODO send payload to filter data
#             # Parsing json and validating
#
#             # json_data = request.get_json()
#             # print(json_data)
#             # # Check body exist
#             # if not json_data:
#             #     return {"message": "No input data provided"}, 400
#         try:
#             input_json = gempy_controller.input_data_to_json(geoModelUrn,
#                                                              data_list=None)
#         except KeyError as err:
#             return {'message': 'No model is loaded yet. Use /operations - to load a model'
#                                ' first: ' + str(err)}, 428
#         print(input_json)
#         rpn = Response(json.dumps(input_json), 200, content_type='application/json')
#         rpn.headers['model_state'] = db.df.loc[geoModelUrn, 'm_state']
#         return rpn
#
#
# @api_ns_geomodels.route('/<string:geoModelUrn>/mesh')
# class GeoModelsMeshView(Resource):
#     def post(self, geoModelUrn):
#         """Send from the client a rexfile. This is useful to load meshes data files
#         from the clent. (not part of v 0.1)"""
