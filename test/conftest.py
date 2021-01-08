
# These two lines are necessary only if GemPy is not installed

# These two lines are necessary only if GemPy is not installed

import os
import tempfile

import pytest
from app.application import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    # os.unlink(app.config['DATABASE'])


@pytest.fixture
def server(app):
    app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True




