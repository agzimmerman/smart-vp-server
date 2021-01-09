from marshmallow import Schema, fields
import uuid


class ModelsSchema(Schema):
    """This that something"""
    name = fields.Str(required=True,
                      description='This is marshmallow description',
                      example='TestModel')
    address = fields.Str(required=True,
                         description='Path to a model pickle. Eventually this will become'
                                     'a general address to any database.',
                         example='./test_models/ModelTest.pickle')

    urn = fields.UUID(description='Model Urn', example=str(uuid.uuid4()))


class ModelSchemeDelete(Schema):
    name = fields.Str(required=True,
                      description='This is marshmallow description',
                      example='TestModel')


class OperationSchema(Schema):
    op_name = fields.Str(required=True,
                      description='Name of the operation',
                      example='load')

    op_urn = fields.Str(required=True,
                        description='Number of the operation',
                        example='operation:200')

    parameters = fields.Dict()
