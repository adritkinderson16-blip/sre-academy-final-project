"""Tests for the ShikyBox Flask application."""

from app.app import create_app


def create_client():
    """Create a Flask test client."""
    application = create_app(testing=True)
    return application.test_client()


def test_storefront_displays_products():
    """The storefront should display all ShikyBox products."""
    client = create_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Dog Adventure Box" in response.data
    assert b"Cat Comfort Box" in response.data
    assert b"Small Pet Discovery Box" in response.data


def test_product_details():
    """A valid product page should load."""
    client = create_client()
    response = client.get("/box/dog-adventure")

    assert response.status_code == 200
    assert b"Dog Adventure Box" in response.data
    assert b"Order this ShikyBox" in response.data


def test_unknown_product_returns_404():
    """An unknown product should return HTTP 404."""
    client = create_client()
    response = client.get("/box/not-a-real-box")

    assert response.status_code == 404


def test_health_and_readiness():
    """Health and readiness endpoints should report success."""
    client = create_client()

    health_response = client.get("/health")
    readiness_response = client.get("/ready")

    assert health_response.status_code == 200
    assert health_response.get_json()["status"] == "healthy"

    assert readiness_response.status_code == 200
    assert readiness_response.get_json()["status"] == "ready"


def test_successful_order():
    """A valid order should be confirmed."""
    client = create_client()
    response = client.post("/order/cat-comfort")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "confirmed"
    assert data["product"] == "Cat Comfort Box"
    assert data["price"] == 27.99


def test_failed_order_simulation():
    """A simulated checkout failure should return HTTP 503."""
    client = create_client()
    response = client.post("/order/cat-comfort?fail=true")

    assert response.status_code == 503
    assert response.get_json()["status"] == "failed"


def test_controlled_application_error():
    """The error simulation endpoint should return HTTP 500."""
    client = create_client()
    response = client.get("/simulate/error")

    assert response.status_code == 500
    assert response.get_json()["status"] == "error"


def test_controlled_latency():
    """The latency simulation endpoint should return the selected delay."""
    client = create_client()
    response = client.get("/simulate/latency?seconds=0")

    assert response.status_code == 200
    assert response.get_json()["delay_seconds"] == 0.0


def test_prometheus_metrics():
    """The metrics endpoint should expose ShikyBox metrics."""
    client = create_client()

    client.get("/")
    client.get("/box/dog-adventure")
    client.post("/order/dog-adventure")

    response = client.get("/metrics")
    metrics_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "shikybox_http_requests_total" in metrics_text
    assert "shikybox_request_duration_seconds" in metrics_text
    assert "shikybox_product_views_total" in metrics_text
    assert "shikybox_orders_total" in metrics_text
    assert "shikybox_app_info" in metrics_text
