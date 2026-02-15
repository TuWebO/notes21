from fastapi.testclient import TestClient
from notes21.api.app import app

client = TestClient(app)

def test_grid_endpoint():
    response = client.get("/grid?note=C&octave=4&key=C")
    assert response.status_code == 200

    data = response.json()

    assert data["note"] == "C"
    assert data["key"] == "C"

    # harmonic grid: row 0 (C), column 1 (natural)
    grid = data["grid"]
    assert grid[0][1] == 1

def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()

def test_grid_json_default():
    response = client.get("/grid?note=C&key=C")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

def test_grid_text_format_query():
    response = client.get("/grid?note=C&key=C&format=text")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "7x3 Music Grid" in response.text

def test_grid_text_accept_header():
    response = client.get(
        "/grid?note=C&key=C",
        headers={"accept": "text/plain"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")

def test_invalid_key_json():
    response = client.get("/grid?note=C&key=J")
    assert response.status_code == 400
    assert "Unknown key" in response.json()["detail"]

def test_invalid_note():
    response = client.get("/grid?note=K&key=C")
    assert response.status_code == 400
    assert "Invalid note base name" in response.json()["detail"]

def test_invalid_key_html():
    response = client.get("/grid/view?note=C&key=J")
    assert response.status_code == 400
    assert "Invalid Key" in response.text
    assert "<html>" in response.text

def test_empty_octave_defaults_to_4():
    response = client.get("/grid?note=C&octave=&key=C")
    assert response.status_code == 200
    assert response.json()["octave"] == 4

def test_invalid_octave():
    response = client.get("/grid?note=C&octave=abc&key=C")
    assert response.status_code == 400

def test_grid_view_success():
    response = client.get("/grid/view?note=C&octave=4&key=C")
    assert response.status_code == 200
    assert "<pre>" in response.text
    assert "7x3 Music Grid" in response.text