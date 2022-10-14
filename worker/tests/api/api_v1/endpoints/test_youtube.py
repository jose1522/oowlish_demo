from typing import Dict

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from core.config import settings


@pytest.fixture(scope="module")
def http_uri() -> str:
    """Fixture for http uri"""
    return settings.API_V1_STR + "/youtube/"


@pytest.fixture(scope="module")
def ws_uri(http_uri) -> str:
    """Fixture for websocket uri"""
    return http_uri + "ws"


@pytest.fixture(scope="module")
def payload() -> Dict[str, str]:
    """Fixture for correct payload to be sent to endpoints"""
    return {"url": "https://www.youtube.com/watch?v=-JAFb2bYJSs"}


@pytest.fixture(scope="module")
def bad_payload() -> Dict[str, bool]:
    """Fixture for incorrect payload to be sent to endpoints"""
    return {"url": False}


def test_websocket_endpoint(mock_nlp_inference, client: TestClient, ws_uri, payload):
    """Runs a successful call to the websocket endpoint"""
    with client.websocket_connect(ws_uri) as websocket:
        websocket.send_json(payload)
        data = websocket.receive_json()
        assert data == {"summary": True}


def test_websocket_endpoint_error(
    mock_nlp_inference, client: TestClient, ws_uri, bad_payload
):
    """Runs an unsuccessful call to the websocket endpoint"""
    with client.websocket_connect(ws_uri) as websocket:
        websocket.send_json(bad_payload)
        with pytest.raises(WebSocketDisconnect) as e:
            websocket.receive_json()
        assert e.value.code == 422


def test_http_endpoint(mock_nlp_inference, client: TestClient, http_uri, payload):
    """Runs a successful call to the http endpoint"""
    response = client.post(url=http_uri, json=payload)
    assert response.status_code == 200
    assert response.json() == {"summary": "True"}


def test_http_endpoint_error(
    mock_nlp_inference, client: TestClient, http_uri, bad_payload
):
    """Runs an unsuccessful call to the http endpoint"""
    response = client.post(url=http_uri, json=bad_payload)
    assert response.status_code == 422
