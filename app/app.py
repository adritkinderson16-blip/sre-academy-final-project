"""ShikyBox pet subscription storefront with Prometheus instrumentation."""

import os
import time

from flask import Flask, Response, abort, jsonify, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.catalog import get_all_products, get_product
from app.metrics import (
    HTTP_ERRORS,
    HTTP_REQUESTS,
    ORDER_FAILURES,
    ORDERS,
    ORDERS_IN_PROGRESS,
    PRODUCT_VIEWS,
    REQUEST_DURATION,
    initialize_app_info,
)


def create_app(testing=False):
    """Create and configure the ShikyBox Flask application."""
    application = Flask(__name__)
    application.config["TESTING"] = testing

    environment = os.getenv("ENVIRONMENT", "development")
    version = os.getenv("APP_VERSION", "1.0.0")
    initialize_app_info(environment=environment, version=version)

    @application.before_request
    def start_request_timer():
        """Record the request start time."""
        request.start_time = time.perf_counter()

    @application.after_request
    def record_request_metrics(response):
        """Record request count, duration, and HTTP errors."""
        endpoint = request.endpoint or "unknown"
        duration = time.perf_counter() - request.start_time

        HTTP_REQUESTS.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(response.status_code),
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

        if response.status_code >= 400:
            HTTP_ERRORS.labels(
                endpoint=endpoint,
                status=str(response.status_code),
            ).inc()

        return response

    @application.route("/")
    def storefront():
        """Display the ShikyBox storefront."""
        return render_template(
            "index.html",
            products=get_all_products(),
            environment=environment,
            version=version,
        )

    @application.route("/box/<product_id>")
    def product_details(product_id):
        """Display the details of one ShikyBox product."""
        product = get_product(product_id)

        if product is None:
            abort(404)

        PRODUCT_VIEWS.labels(box_type=product["pet_type"]).inc()
        return render_template("product.html", product=product)

    @application.route("/order/<product_id>", methods=["POST"])
    def place_order(product_id):
        """Simulate a successful or failed ShikyBox purchase."""
        product = get_product(product_id)

        if product is None:
            abort(404)

        should_fail = request.args.get("fail", "false").lower() == "true"

        ORDERS_IN_PROGRESS.inc()
        try:
            time.sleep(0.25)

            if should_fail:
                ORDER_FAILURES.labels(
                    box_type=product["pet_type"],
                    reason="simulated_checkout_failure",
                ).inc()

                return (
                    jsonify(
                        {
                            "status": "failed",
                            "message": "The simulated checkout failed.",
                            "product": product["name"],
                        }
                    ),
                    503,
                )

            ORDERS.labels(box_type=product["pet_type"]).inc()

            return jsonify(
                {
                    "status": "confirmed",
                    "message": "Your ShikyBox order was created.",
                    "product": product["name"],
                    "price": product["price"],
                }
            )
        finally:
            ORDERS_IN_PROGRESS.dec()

    @application.route("/about")
    def about():
        """Display information about the ShikyBox project."""
        return render_template(
            "about.html",
            environment=environment,
            version=version,
        )

    @application.route("/health")
    def health():
        """Kubernetes liveness endpoint."""
        return jsonify(
            {
                "status": "healthy",
                "service": "shikybox",
                "version": version,
            }
        )

    @application.route("/ready")
    def ready():
        """Kubernetes readiness endpoint."""
        return jsonify(
            {
                "status": "ready",
                "service": "shikybox",
            }
        )

    @application.route("/metrics")
    def metrics():
        """Expose metrics in Prometheus text format."""
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    @application.route("/simulate/error")
    def simulate_error():
        """Generate a controlled HTTP 500 response."""
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Simulated ShikyBox application error.",
                }
            ),
            500,
        )

    @application.route("/simulate/latency")
    def simulate_latency():
        """Generate a controlled slow response."""
        try:
            delay = float(request.args.get("seconds", "2"))
        except ValueError:
            delay = 2.0

        delay = max(0.0, min(delay, 5.0))
        time.sleep(delay)

        return jsonify(
            {
                "status": "completed",
                "delay_seconds": delay,
            }
        )

    return application


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        debug=False,
    )
