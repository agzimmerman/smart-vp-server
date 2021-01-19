"""
Interface module to the business logic
"""

from app.logic.model_manager import ModelLoader, ModelsIndex
import numpy as np

# Initialize db for docker.csv
db = ModelsIndex('docker.csv', path_to_cache=0)

# Init db for local
#db = ModelsIndex('fixture.csv', path_to_cache=1)


class OperationController:
    def __init__(self):
        self.geo_models_dict = dict()

    def parse(self, **kwargs):

        operation_name = kwargs.get('op_name')
        if operation_name is None:
            raise KeyError('Operations needs a name.')

        if operation_name == 'edit':
            # self.editGemPy(**kwargs['parameters'])
            pass
        elif operation_name == 'load':
            # self.loadGemPy(**kwargs['parameters'])
            pass

    @staticmethod
    def _add_model_state(modelUrn):
        """Add counter to the model.

        Notes:
            At the moment 23.07.2020 is not persistent

        """
        db.df.loc[modelUrn, "m_state"] += 1
