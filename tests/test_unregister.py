def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/participants"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        activity_path,
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }

    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_path = "/activities/Unknown%20Club/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        activity_path,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_for_student_not_signed_up(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/participants"
    email = "absent.student@mergington.edu"

    # Act
    response = client.delete(
        activity_path,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}