"""
This module test the database functionality
"""
import os
from app.logic.model_manager import ModelsIndex, ModelLoader
import pytest

current_path = os.path.dirname(__file__)


@pytest.fixture(scope='session')
def db_pickles():
    # Creates an empty table. Fixture is the cache file
    db = ModelsIndex('fixture.csv', read_cache=False)

    # Add the entry TestModel. This will create a new uuid
    db.add_entry(name='TestModel', address=current_path + '/../data/fault_test.pickle')
    return db


def test_add_entry():
    """Test if to add new entries in the database"""
    db = ModelsIndex('test_add_entry', read_cache=False)

    # Test wrong address
    with pytest.raises(AttributeError):
        db.add_entry(name='TestModel', address='./test_models')

    # Test add entry
    db.add_entry(name='Random', address=current_path+'/../data/fault_test.pickle',
                 write_cache=False)

    # Test trying to add the same entry twice
    with pytest.raises(ValueError):
        db.add_entry(name='Random', address=current_path + '/../data/fault_test.pickle')
    print(db.df)


def test_delete_entry():
    """Test delete entry by modelUrn"""
    db = ModelsIndex('test_delete_entry', read_cache=False, path_to_cache=0)
    db.add_entry(name='Random', address=current_path + '/../data/fault_test.pickle',
                 write_cache=False)
    db.delete_entry('model:Random')


def test_loader(db_pickles):
    """Load into memory a GemPy model"""
    loader = ModelLoader(db_pickles)

    # Geomodel is already a gempy object
    geo_model = loader.load_model('model:TestModel')
    print(geo_model)


def test_db_get_table(db_pickles):
    """Get the _models in the index. These are the valid names we can pass
    to load_model"""
    table = ModelsIndex('fixture.csv').get_table()
    print(table)
