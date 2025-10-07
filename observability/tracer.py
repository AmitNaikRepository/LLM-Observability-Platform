from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_telemetry(app):
    """Configure OpenTelemetry tracing"""

    # Create resource with service information
    resource = Resource.create({
        "service.name": "llm-observability-api",
        "service.version": "1.0.0"
    })

    # Setup trace provider
    trace_provider = TracerProvider(resource=resource)

    # Configure OTLP exporter (sends to Jaeger)
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )

    # Add span processor
    trace_provider.add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )

    # Set global trace provider
    trace.set_tracer_provider(trace_provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    return trace.get_tracer(__name__)
