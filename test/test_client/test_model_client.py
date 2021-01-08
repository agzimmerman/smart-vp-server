"""
This module test the api from the client side. This means that gets the
errors that the client sees
"""
import json
import os

current_path = os.path.dirname(__file__)


def test_model_db_get(client):
    """Get index values"""
    rpn = client.get('/geomodels/', follow_redirects=True)
    print(rpn.data)
    print(rpn)


def test_model_db_post(client):
    # Test add a value with the wrong args (path) to the index
    rpn_post_wrong_data = client.post('/geomodels/',
                                      data=json.dumps({'name': 'TestModel',
                                                       'path': './test_models'}),
                                      content_type='application/json',
                                      follow_redirects=True)

    print('Response in post: ', rpn_post_wrong_data, rpn_post_wrong_data.data, '\n\n')
    assert rpn_post_wrong_data.status_code == 422

    # Add a new right value to the index
    rpn_post = client.post('geomodels/',
                           data=json.dumps({
                               'name': 'TestModelClient',
                               'address': current_path + '/../data/fault_test.pickle'}),
                           content_type='application/json',
                           follow_redirects=True)

    print('Response in post', rpn_post, rpn_post.data)
    assert rpn_post.status_code == 201

    # Get the new index with the new value
    rpn_get = client.get('/geomodels/')
    print('Response in client after add: ', rpn_get, rpn_get.data)

    # Delete the new value
    rpn_post2 = client.delete('/geomodels/model:TestModelClient',
                              data=json.dumps({
                              }),
                              content_type='application/json',
                              follow_redirects=True)

    assert rpn_post2.status_code != 422
    print('Response in post', rpn_post2, rpn_post2.data, '\n\n')

    # Get the index again with just the default value
    rpn_get2 = client.get('/geomodels/')
    print('Response in client after delete: ', rpn_get2, rpn_get2.data, '\n\n')


# def test_model_loader(client):
#     # Get the current urn - This has to be empty since not mode
#     urn_dict = client.get('/_geomodels/loader',
#                           follow_redirects=True)
#
#     print('Empty dict: ', urn_dict.data, '\n\n')
#
#     # Load a given model defined by the uuid - rpn contains already the urn
#     rpn = client.post('/_geomodels/loader',
#                       data=json.dumps({'name': 'TestModel'}),
#                       content_type='application/json',
#                       follow_redirects=True)
#     print(rpn, rpn.data)
#     rpn_dict = json.loads(rpn.json)
#
#     # Test the loader get
#     urn_dict_json = client.get('/_geomodels/loader',
#                                follow_redirects=True)
#
#     urn_dict = json.loads(urn_dict_json.json)
#     urn = urn_dict['TestModel']['uuid']
#     print(urn_dict, '\n\n')
#     assert rpn_dict['urn'] == urn
#
#     # Retrieve the rexfile:
#     rpn2 = client.get('/_geomodels/' + urn)
#     assert len(rpn2.data) == 356426
#     print(rpn2, len(rpn2.data))
