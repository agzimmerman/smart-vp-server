"""
This module test the api from the server side. This means that gets the
errors that at the server side
"""
import gempy

from app.application.geomodels.routes import GeoModelsIndexView, GeoModelView
import pytest
import json
import os

from app.logic.func_api import db
from app.logic.model_manager import ModelLoader, ModelsIndex

data_path = os.path.dirname(__file__) + '/../data/'


print(data_path)

# test_db = ModelsIndex('fixture.csv', path_to_cache=1)
test_db = ModelsIndex('docker.csv', path_to_cache=0)


class TestModelsDB:

    def test_get_model_ids(self):
        """Get the index"""
        m_id = GeoModelsIndexView().get()
        print(m_id)

    def test_post_ids(self, app):
        """
        Add new entry to the index.

        Args:
            app:
        """
        with app.test_request_context(path='/',
                                      json={
                                          'name': 'TestModel_temp',
                                          'address': data_path + 'fault_test.pickle'}):

            mdb = GeoModelsIndexView()

            # Test post
            rpn = mdb.post()
            print('response: ', rpn)

            # Test get and right that post worked
            assert mdb.get()["model:TestModel_temp"]["name"] == "TestModel_temp"

        # Now we want to delete that entry
        with app.test_request_context(path='/',
                                      json={}):

            # Test delete
            model_ = GeoModelView()

            rpn = model_.delete('model:TestModel_temp')

            print('response 2: ', rpn)
            # assert len(mdb.get()) == 1
        return mdb


class TestLoading:
    def test_loading(self):
        loader = ModelLoader(test_db)
        loader.load_model("model:TestModel")

    def test_remote(self):
        loader = ModelLoader(test_db)
        g = loader.load_model("model:Graben")
        #gempy.compute_model(g[0])
        #gempy.plot_3d(g[0], image=True)
        print(g)



