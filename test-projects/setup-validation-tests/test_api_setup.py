import httpx

def test_api_client_dependancy_is_ready():
    response = httpx.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1