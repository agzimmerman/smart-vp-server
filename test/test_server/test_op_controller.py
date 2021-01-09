import os
from app.application.geomodels.routes import GeoModelsOperationsView, GeoModelsOutputView
from app.logic.func_api import GemPyController
from app.logic.model_manager import ModelsIndex

current_path = os.path.dirname(__file__)


class TestOpsController:
    def test_op_load_model(self, app):
        ops = GeoModelsOperationsView()
        with app.test_request_context(path='model:test/operations',
                                      json={'op_name': 'load',
                                            'op_urn': 'operation:201'}):

            op_urn = ops.post('modelUrn')
            print(op_urn)

            # Test bad request
            assert op_urn[1] == 400

        with app.test_request_context(path='geomodel:test/operations',
                                      json={'op_name': 'load',
                                            'op_urn': 'operation:201',
                                            'parameters': {
                                                'modelUrn': 'model:TestModel'
                                            }}):
            op_urn = ops.post('modelUrn')
            print(op_urn)
            assert op_urn[1] == 202
            
    def test_op_load_model2(self, app):
        
        ops = GeoModelsOperationsView()
        
        with app.test_request_context(
                path='geomodel:test/operations',
                json={'op_name': 'load',
                      'op_urn': 'operation:201',
                      'parameters': {'modelUrn': 'model:TestModel2'}}):
            
            stuff  = ops.post('modelUrn')
            
            print(stuff)
            
            assert stuff[1] == 202


class TestIO:
    def test_get_output(self, app):

        model_out = GeoModelsOutputView()
        ops = GeoModelsOperationsView()

        # Trying to get rexfile before loading
        resp = model_out.get(None)
        try:
            code = resp[1]
        except TypeError:
            code = resp.status

        print("If the all test are ran together, the response should be a 200,"
              "otherwise, if the model is ran alone 428. HTML code: ", code)

        # Loading model
        with app.test_request_context(path='model:TestModel/operations',
                                      json={'op_name': 'load',
                                            'op_urn': 'operation:201',
                                            'parameters': {
                                                'modelUrn': 'model:TestModel'
                                            }}):

            op_urn = ops.post('model:TestModel')
            resp = model_out.get('model:TestModel')
            print(resp)

    def test_get_input(self, app):
        gempy_controller = GemPyController()
        gempy_controller.operation_controller.loadGemPy(**{
            'modelUrn': 'model:TestModel'
        })

        json_rpn = gempy_controller.input_data_to_json('model:TestModel')
        # print(json_rpn)
        assert json_rpn['sp'][20]['Y'] == 800







