# Rest libraries
from flask import json, request, Response
from app.apis.namespaces import api_ns_smart_vp
from flask_restx import Resource
from marshmallow import ValidationError
from marshmallow_jsonschema import JSONSchema

# Additional libraries

# Importing modules
from .schemas import ModelsSchema, ModelSchemeDelete, OperationSchema
from ...logic.SmartVPController import SmartVPController
from ...logic.func_api import OperationController, db

# Defining models

# Init the JSON schema
models_schema_input = ModelsSchema()
model_schema_del = ModelSchemeDelete()

# Create a doc for SWAGGER from the schema
models_schema_input_doc = api_ns_smart_vp.schema_model(
    'models_schema_input_doc',
    JSONSchema().dump(
        models_schema_input)['definitions'][
        'ModelsSchema'])

# Business logic classes
operation_controller = OperationController()
smart_vp_controller = SmartVPController()

# TODO operations has to be a dictionary with keys: operationUrn!
operation_status = dict()  # running or finished

op_schema = OperationSchema()
op_schema_doc = api_ns_smart_vp.schema_model(
    'models_operations_schema_doc',
    JSONSchema().dump(
        op_schema)['definitions'][
        'OperationSchema'])


@api_ns_smart_vp.route('/')
class GeoModelsIndexView(Resource):
    @api_ns_smart_vp.doc()
    def get(self):
        """Returns a list of all geomodel available for loading"""
        path = "/home/smartVP/SMART_VP_server/test/data/cache_db/workspace.json"
        with open(path) as json_file:
            data = json.load(json_file)

        rpn = Response(json.dumps(data), 200, content_type='application/json')
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/wells_header')
class SmartWellsView1(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            wells_dict = smart_vp_controller.file_to_subsurface_wells()[1]
        except KeyError as err:
            return {'message': str(err)}, 428
        print(wells_dict)
        rpn = Response(json.dumps(wells_dict), 200, content_type='application/json')
        # rpn.headers['model_state'] = db.df.loc[geoModelUrn, 'm_state']
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/wells_body')
class SmartWellsView2(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            wells_binary = smart_vp_controller.file_to_subsurface_wells()[0]
        except KeyError as err:
            return {'message': str(err)}, 428
        rpn = Response(wells_binary, 200)
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/volume_header')
class SmartVolumeView1(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            volume_dict = smart_vp_controller.file_to_subsurface_volume()[1]
        except KeyError as err:
            return {'message': str(err)}, 428
        print(volume_dict)
        rpn = Response(json.dumps(volume_dict), 200, content_type='application/json')
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/volume_body')
class SmartVolumeView2(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            volume_binary = smart_vp_controller.file_to_subsurface_volume()[0]
        except KeyError as err:
            return {'message': str(err)}, 428
        rpn = Response(volume_binary, 200)
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/collars_header')
class SmartCollarsView1(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            collars_dict = smart_vp_controller.file_to_subsurface_collars()[1]
        except KeyError as err:
            return {'message': str(err)}, 428
        print(collars_dict)
        rpn = Response(json.dumps(collars_dict), 200, content_type='application/json')
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/collars_body')
class SmartCollarsView2(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            collars_binary = smart_vp_controller.file_to_subsurface_collars()[0]
        except KeyError as err:
            return {'message': str(err)}, 428
        rpn = Response(collars_binary, 200)
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/surfaces_header')
class SmartSurfacesView1(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            surfaces_dict = smart_vp_controller.file_to_subsurface_surfaces()[1]
        except KeyError as err:
            return {'message': str(err)}, 428
        print(surfaces_dict)
        rpn = Response(json.dumps(surfaces_dict), 200, content_type='application/json')
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/surfaces_body')
class SmartSurfacesView2(Resource):
    @api_ns_smart_vp.doc(body=None,  # TODO add schema to filte data
                         responses={200: 'json'})
    def get(self, geoModelUrn):
        """Get gempy input data in json. With a payload (to be defined) we can
        filter how much data is sent"""

        try:
            surfaces_binary = smart_vp_controller.file_to_subsurface_surfaces()[0]
        except KeyError as err:
            return {'message': str(err)}, 428
        rpn = Response(surfaces_binary, 200)
        return rpn


@api_ns_smart_vp.route('/<string:geoModelUrn>/operations')
class SmartOperationsView(Resource):
    @api_ns_smart_vp.doc(body=op_schema_doc,
                         responses={202: 'Operation Urn'})
    def post(self, geoModelUrn):
        """Applies an operation. All the model manipulation happen here.
        body is a json

        :returns
            Operation Urn
        """
        # Parsing json and validating
        json_data = request.get_json()
        print(json_data)
        # Check body exist
        if not json_data:
            return {"message": "No input data provided"}, 400

        # Check format of the body
        try:
            json_data = op_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        operation_status[json_data['op_urn']] = 'running'

        # Need a parser function: That decide what to do with each operation
        try:
            operation_controller.parse(**json_data)
        except Exception as err:
            return {'Error raised during processing: ': err}, 400

        operation_status[json_data['op_urn']] = 'finished'
        print(json_data['op_urn'])

        # Probably I can pass back the operation urn without having the deserialize it
        return {'Operation Urn': json_data['op_urn']}, 202
