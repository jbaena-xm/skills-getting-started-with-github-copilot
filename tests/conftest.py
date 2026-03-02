import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    # Arrange
    original_activities = copy.deepcopy(activities)

    # Act
    with TestClient(app) as test_client:
        yield test_client

    # Assert
    activities.clear()
    activities.update(original_activities)
