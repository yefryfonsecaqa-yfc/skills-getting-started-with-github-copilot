def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_static_index_is_available(client):
    # Arrange
    expected_title = "Mergington High School"

    # Act
    response = client.get("/static/index.html")

    # Assert
    assert response.status_code == 200
    assert expected_title in response.text
