from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource
from prometheus_client import start_http_server

# Custom metrics
llm_request_counter = None
llm_response_time = None
llm_token_counter = None

def setup_metrics():
    """Configure OpenTelemetry metrics with Prometheus"""

    # Create resource
    resource = Resource.create({
        "service.name": "llm-observability-api"
    })

    # Setup Prometheus exporter
    prometheus_reader = PrometheusMetricReader()

    # Create meter provider
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[prometheus_reader]
    )

    # Set global meter provider
    metrics.set_meter_provider(meter_provider)

    # Get meter
    meter = metrics.get_meter(__name__)

    # Define custom metrics
    global llm_request_counter, llm_response_time, llm_token_counter

    llm_request_counter = meter.create_counter(
        name="llm_requests_total",
        description="Total number of LLM requests",
        unit="1"
    )

    llm_response_time = meter.create_histogram(
        name="llm_response_time_seconds",
        description="LLM response time in seconds",
        unit="s"
    )

    llm_token_counter = meter.create_counter(
        name="llm_tokens_total",
        description="Total tokens used",
        unit="1"
    )

    # Start Prometheus metrics server on port 8001
    start_http_server(port=8001)

    return meter
