from fastapi.testclient import TestClient
from examples.app import app

client = TestClient(app)

# Test data
VALID_API_KEY = "DEN#3xTezZDo1nJg1pO$tIrzQ9A"
INVALID_API_KEY = "invalid_key"


def test_root_endpoint():
    """Test the root endpoint returns correct welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_public_endpoint():
    """Test the public endpoint is accessible without API key"""
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {
        "message": "This is a public endpoint accessible to everyone."
    }


def test_admin_endpoint_with_valid_api_key():
    """Test the admin endpoint with valid API key"""
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.get("/secure/admin", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the admin area!"}


def test_admin_endpoint_without_api_key():
    """Test the admin endpoint without API key should fail"""
    response = client.get("/secure/admin")
    assert response.status_code == 403


def test_admin_endpoint_with_invalid_api_key():
    """Test the admin endpoint with invalid API key should fail"""
    headers = {"X-API-Key": INVALID_API_KEY}
    response = client.get("/secure/admin", headers=headers)
    assert response.status_code == 403


def test_settings_endpoint_with_valid_api_key():
    """Test the settings endpoint with valid API key"""
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.get("/secure/settings", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Settings page, accessible only to authorized users."
    }


def test_settings_endpoint_without_api_key():
    """Test the settings endpoint without API key should fail"""
    response = client.get("/secure/settings")
    assert response.status_code == 403


def test_settings_endpoint_with_invalid_api_key():
    """Test the settings endpoint with invalid API key should fail"""
    headers = {"X-API-Key": INVALID_API_KEY}
    response = client.get("/secure/settings", headers=headers)
    assert response.status_code == 403
