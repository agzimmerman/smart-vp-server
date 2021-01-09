import pathlib
import os
# os.environ["THEANO_FLAGS"] = "mode=FAST_RUN,device=cuda"
import pandas as pd
import uuid as uuid_m
from typing import Union
from pathlib import Path

import pooch

path_to_cache_default_test = os.path.dirname(__file__) + '/../../test/data/cache_db/'

# To find the cache file in docker.csv
file = Path(path_to_cache_default_test)
if True:
    path_to_cache_default = "/home/gempy/work/gempy_server/test/data/cache_db/"


class ModelsIndex:
    """ Class tha handles the stored _models
    """

    def __init__(self, db_name: object, read_cache: object = True,
                 path_to_cache=0) -> object:
        file_not_found = False

        if path_to_cache == 0:
            self.path_to_cache = path_to_cache_default
        elif path_to_cache == 1:
            self.path_to_cache = path_to_cache_default_test
        else:
            self.path_to_cache = path_to_cache
        self.db_name = db_name
        if read_cache:
            try:
                self._read_cache(db_name)
            except FileNotFoundError:
                file_not_found = True
        if read_cache is False or file_not_found:
            self.df = pd.DataFrame(columns=['name', 'm_state', 'address', 'uuid', 'loaded'])
            # TODO: add types str, str, int, str, bool

            self.df.rename_axis(index='modelUrn', inplace=True)

    def _write_cache(self):
        df_aux = self.df.copy()
        df_aux.to_csv(self.path_to_cache + self.db_name)

    def _read_cache(self, db_name):
        self.df = pd.read_csv(self.path_to_cache + db_name, index_col=0)
        return self.df

    @staticmethod
    def _check_address(address):
        file = Path(address)
        if not file.is_file():
            raise AttributeError('Wrong address')
        return True

    def get_table(self, db_name=None):
        if db_name is None:
            db_name = self.db_name
        return self._read_cache(db_name)

    def add_entry(self, name: str, address: str, modelUrn:str =None,
                  uuid=None, write_cache=True, **kwargs):
        """


        Args:
            name:
            address:
            modelUrn:
            uuid:
            write_cache:
            **kwargs:

        Returns:

        Notes:
            At the moment is not over writing.
        """

        if modelUrn is None:
            # Adding first word
            modelUrn = 'model:'+name.split()[0]

        self._check_address(address)

        if uuid is None:
            uuid = str(uuid_m.uuid4())

        entry = {'name': name, 'm_state': 0, 'address': address, 'uuid': uuid, 'loaded': False}
        entry.update(kwargs)
        if type(modelUrn) == str:
            table_index = [modelUrn]

        entry_df = pd.DataFrame(entry, index=table_index)

        try:
            self.df = pd.concat([self.df, entry_df],
                                ignore_index=False, verify_integrity=True)
        except ValueError as e:
            raise ValueError(e)

        self.df.rename_axis(index='ModelUrn', inplace=True)

        if write_cache:
            self._write_cache()
        return self.df

    def delete_entry(self, modelUrn, cache=True, **kwargs):
        self.df.drop(modelUrn, inplace=True)

        if cache:
            self._write_cache()
        return self.df

    def change_state(self):
        """So far the state is only add +1. Not worth it to over engineer this"""
        raise NotImplementedError


class ModelLoader:
    """Class to store _models and metadata under a unique identifier.
    The identifier is part of the endpoint path which is dynamically generated for each model.
    """

    def __init__(self, model_db: ModelsIndex):
        self.urn_dict = {}
        self.active_model = 'Not Loaded yet'
        self.model = None

        self.model_db = model_db


    def get_models(self):
        return self.model_db.df

    def add_model(self, **kwargs):
        return self.model_db.add_entry(**kwargs)


