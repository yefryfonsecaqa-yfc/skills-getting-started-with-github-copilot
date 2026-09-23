import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import activities, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_duplicate_student_cannot_register_for_same_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"
    assert activities[activity_name]["participants"].count(email) == 1


def test_student_can_be_unregistered_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unknown_activity_cannot_unregister_student():
    response = client.delete(
        "/activities/Unknown Activity/signup?email=student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregistered_student_cannot_be_removed():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
