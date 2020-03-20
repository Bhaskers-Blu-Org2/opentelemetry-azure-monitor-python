from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

from azure_monitor import AzureMonitorSpanExporter


# Callback function to add os_type: linux to span properties
def callback_function(envelope):
    envelope.data.base_data.properties["os_type"] = "linux"
    return True


exporter = AzureMonitorSpanExporter(
    connection_string="InstrumentationKey=<INSTRUMENTATION KEY HERE>"
)
exporter.add_telemetry_processor(callback_function)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchExportSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("hello"):
    print("Hello, World!")

input("Press any key to exit...")
