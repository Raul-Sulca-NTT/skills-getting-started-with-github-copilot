def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/signup"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        activity_path,
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up new.student@mergington.edu for Chess Club"
    }

    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_path = "/activities/Unknown%20Club/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        activity_path,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/signup"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        activity_path,
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}