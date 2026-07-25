from fastapi.testclient import TestClient
import sys
import os

# Ensure the app can find the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import your FastAPI app instance (adjust 'src.main' if your app is named differently)
from src.main import app 

client = TestClient(app)

def test_api_health():
    """Verify that the FastAPI backend is up and running."""
    response = client.get("/")
    # Assuming your root endpoint returns a 200 OK status
    assert response.status_code == 200
    
    # If your root endpoint returns a specific JSON message, you can test it like this:
    # assert "message" in response.json()