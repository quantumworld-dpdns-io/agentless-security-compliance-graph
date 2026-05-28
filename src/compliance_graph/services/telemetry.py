
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class TelemetryService:
    """OpenTelemetry integration for compliance graph observability."""

    def __init__(self, service_name: str = "compliance-graph", otel_endpoint: str = "http://localhost:4317"):
        self.service_name = service_name
        self.otel_endpoint = otel_endpoint
        self.tracer: trace.Tracer | None = None
        self.meter: metrics.Meter | None = None
        self._initialize()

    def _initialize(self):
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": "0.1.0",
            "deployment.environment": "production",
        })
        trace_provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(endpoint=self.otel_endpoint, insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(trace_provider)
        self.tracer = trace.get_tracer(self.service_name)

        meter_provider = MeterProvider(resource=resource)
        metrics.set_meter_provider(meter_provider)
        self.meter = metrics.get_meter(self.service_name)

    def create_span(self, name: str, attributes: dict | None = None):
        if self.tracer:
            return self.tracer.start_as_current_span(name, attributes=attributes)
        from contextlib import nullcontext
        return nullcontext()

    def record_metric(self, name: str, value: float, unit: str = "1"):
        if self.meter:
            counter = self.meter.create_counter(name, unit=unit, description=f"Metric: {name}")
            counter.add(value)

    async def trace_scan(self, scan_type: str, target: str):
        with self.create_span(f"scan.{scan_type}", {"target": target}):
            return {"traced": True, "scan_type": scan_type, "target": target}
