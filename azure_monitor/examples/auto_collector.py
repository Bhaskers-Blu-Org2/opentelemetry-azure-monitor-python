# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from azure_monitor import AutoCollection, AzureMonitorMetricsExporter
from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, Meter
from opentelemetry.sdk.metrics.export.controller import PushController

metrics.set_preferred_meter_implementation(lambda _: Meter())
meter = metrics.get_meter(__name__)
exporter = AzureMonitorMetricsExporter(
    connection_string="InstrumentationKey=<INSTRUMENTATION KEY HERE>"
)
controller = PushController(meter, exporter, 5)

testing_label_set = meter.get_label_set({"environment": "testing"})

# Automatically collect standard metrics
auto_collection = AutoCollection(
    meter=meter,
    label_set=testing_label_set,
    collection_interval=120,  # Collect every 2 minutes
)

input("Press any key to exit...")
