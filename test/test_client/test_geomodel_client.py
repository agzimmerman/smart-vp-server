import json
import os
import pytest

current_path = os.path.dirname(__file__)


@pytest.fixture
def load_model(client):
    # test op:load model
    rpn = client.post('/geomodels/model:Graben/operations',
                      data=json.dumps(
                          {
                              'op_name': 'load',
                              'op_urn': 'operation:1234',
                              'parameters': {
                                  'modelUrn': 'model:Graben'
                              }

                          }
                      ),
                      follow_redirects=True,
                      content_type='application/json'
                      )

    assert rpn.status_code == 202
    print(rpn)


def test_post_op_edit(client, load_model):
    client.post('/geomodels/model:Graben/operations',
                data=json.dumps(
                    {
                        'op_name': 'edit',
                        'op_urn': 'operation:1234',
                        'parameters':
                        {
                            "modelUrn": "model:Graben",
                            # "data_object": "surface_points",
                            "method": "modify_surface_points",
                            "indices": 0,
                            "X": 5,
                            "Z": -100
                        }

                    }
                ),
                follow_redirects=True,
                content_type='application/json'
                )
    # Test if the counter went up
    rpn = client.get('/geomodels/', follow_redirects=True)
    print(rpn.data)
    print(rpn)


# @pytest.mark.skip(msg='Mocking is not working')
# def test_get_rexfile(client, load_model):
#
#     # Test get output
#     rpn_io = client.get('/geomodels/model:Graben/output')
#     print(rpn_io)
#     # This is for one layer: assert len(rpn_io.data) == 356426
#     assert len(rpn_io.data) == 760214


def test_get_input(client, load_model):
    # Test get input
    rpn_io = client.get('/geomodels/model:TestModel/input')
    print(rpn_io)