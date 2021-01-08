import time

import requests
import pytest
import json

base_url = 'http://127.0.0.1:5000/'


@pytest.mark.skipif(True, reason="no way of currently testing this")
class TestAsync:
    def test_get_models_list(self):
        rpn = requests.get(base_url + 'geomodels/')
        print(rpn)

    def test_connect_to_server(self):
        rpn = requests.get(base_url)
        print(rpn)

    def test_get_rex_async(self):

        # Make a request. If after .5s is not done keep going
        try:
            rpn = requests.post(base_url + 'geomodels/test/operations',
                                json={
                                    'op_name': 'load',
                                    'op_urn': 'operation:1234',
                                    'parameters': {
                                        'modelUrn': 'model:TestModel'
                                    }

                                }
                                , timeout=0.5)
        except requests.exceptions.Timeout:
            pass

        print('foo')

        # Check if the op is still running
        op_status = requests.get(base_url + 'geomodels/test/operations/operation:1234/status')
        print(op_status, op_status.json())

        # Testing wait for the operation to end
        time_waiting = 0.

        op_running = True
        while op_running:
            op_status = requests.get(base_url + 'geomodels/test/operations/operation:1234/status')
            if op_status.json()['OpStatus'] == 'running':
                op_running = True
                time.sleep(1)
                time_waiting += op_status.elapsed.seconds + 1
            else:
                op_running = False
                rex_file = requests.get(base_url + 'geomodels/test/output')

        print('Time elapsed: ', time_waiting)

        print('Rexfile: ', rex_file)

    def test_get_rex(self):
        rex_file = requests.get(base_url + 'geomodels/test/output')

