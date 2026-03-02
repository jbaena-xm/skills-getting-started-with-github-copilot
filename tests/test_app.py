from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_dictionary(client):
    # Arrange
    expected_key = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert expected_key in payload


def test_signup_for_activity_adds_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_for_activity_returns_not_found_for_missing_activity(client):
    # Arrange
    missing_activity_name = "Nonexistent Club"
    encoded_activity_name = quote(missing_activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_rejects_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_removes_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{encoded_activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_from_activity_returns_not_found_for_missing_activity(client):
    # Arrange
    missing_activity_name = "Nonexistent Club"
    encoded_activity_name = quote(missing_activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{encoded_activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_rejects_student_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(f"/activities/{encoded_activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
