"""
Interface module to the business logic
"""

from app.logic.model_manager import ModelLoader, ModelsIndex
import gempy as gp
import numpy as np
from gempy.addons.gempy_to_rexfile import GemPyToRex

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
            self.edit(**kwargs['parameters'])

        elif operation_name == 'load':
            self.load(**kwargs['parameters'])

    def load(self, **param):
        try:
            modelUrn = param.get('modelUrn')
            loader = ModelLoader(db)
            # Check if the model has been loaded already
            if modelUrn not in self.geo_models_dict:

                geo_model, _engineUrn = loader.load_model(modelUrn)
                self.geo_models_dict[modelUrn] = geo_model
                # Recomputing the model
                gp.compute_model(self.geo_models_dict[modelUrn])
            
        except KeyError as e:
            print('The address to the model is wrong: ' + str(e))
            return {'The name provided does not exist on the index: ' + str(e), 400}

        except Exception as e:
            print('The address to the model is wrong: ' + str(e))
            return {'The address to the model is wrong: ' + str(e), 400}

    def edit(self, **param):
        """Edit the gempy geomodel compute the model and create rexfile

        Notes:
            Change the model state

        """

        modelUrn = param.pop('modelUrn')

        if 'data_object' in param:
            data_object = param.pop('data_object')
        else:
            data_object=None
        method = param.pop('method')

        # Editing the model
        print('I am in editing')
        gp.edit(self.geo_models_dict[modelUrn], method, data_object, **param)

        print('I am in computing the model')
        # Recomputing the model
        gp.compute_model(self.geo_models_dict[modelUrn])

        # Add model state
        print('I am at add model state')
        self._add_model_state(modelUrn)
        # print(self.geo_models_dict[modelUrn])

    @staticmethod
    def _add_model_state(modelUrn):
        """Add counter to the model.

        Notes:
            At the moment 23.07.2020 is not persistent

        """
        db.df.loc[modelUrn, "m_state"] += 1


class GemPyController:
    """Container class to be the first layer of logic between the REST and GemPy

    """

    def __init__(self, op_controller: OperationController = None):

        if op_controller is None:
            self.operation_controller = OperationController()
        else:
            self.operation_controller = op_controller

        # self.gempy_to_rex = geomodel_to_rex
        self.gempy_to_rex = GemPyToRex()
        self.geo_models_dict = self.operation_controller.geo_models_dict

    def input_data_to_json(self, geomodel_urn, data_list: list = None):
        """Append all GemPy data structures in one json file

        Returns:
        json
        """
        if data_list is None:
            data_list = ['surface_points', 'orientations', 'surfaces']

        # data_json = json.loads('{}')#str()
        data_dict = dict()

        model = self.geo_models_dict[geomodel_urn]
        for data_item in data_list:
            if 'surface_points' == data_item:
                sp_col = ['X', 'Y', 'Z', 'surface']
                data_dict['sp'] = model.surface_points.df[sp_col].to_dict(orient='index')
            elif 'orientations' == data_item:
                o_col = ['X', 'Y', 'Z', 'surface',
                         'G_x', 'G_y', 'G_z',
                         'azimuth', 'dip', 'polarity']
                data_dict['orientations'] = model.orientations.df[o_col].to_dict(orient='index')
            elif 'surfaces' == data_item:
                s_col = ['surface', 'series', 'color', 'id']
                data_dict['surfaces'] = model.surfaces.df[s_col].to_dict(orient='index')

        return data_dict

    def encode_rex(self, geomodel_urn, delete_solutions=False):
        """

        Args:
            geomodel_urn:
            delete_solutions (bool): If true delete gempy solutions after compute
             rexfile
            
        Returns:
            bytearray
        """
        model = self.geo_models_dict[geomodel_urn]
        # rex = self.gempy_to_rex(model, backside=False)
        rex = self.gempy_to_rex(model)
        if delete_solutions is True:
            self._delete_solutions(model)
        print(rex[:25])
        return rex
    
    @staticmethod
    def _delete_solutions(geomodel:gp.Project):
        geomodel.solutions.lith_block = np.empty(0)
        geomodel.solutions.scalar_field_matrix = np.array([])
        geomodel.solutions.block_matrix = np.array([])
        geomodel.solutions.mask_matrix = np.array([])
        geomodel.solutions.mask_matrix_pad = []
        geomodel.solutions.values_matrix = np.array([])
        geomodel.solutions.gradient = np.empty(0)

        geomodel.solutions.vertices = []
        geomodel.solutions.edges = []

        geomodel.solutions.geological_map = None
        geomodel.solutions.sections = None
        geomodel.solutions.custom = None
