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