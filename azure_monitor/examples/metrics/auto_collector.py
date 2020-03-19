# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export.controller import PushController

from azure_monitor import AutoCollection, AzureMonitorMetricsExporter

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
exporter = AzureMonitorMetricsExporter(
    connection_string="InstrumentationKey=<INSTRUMENTATION KEY HERE>"
)
controller = PushController(meter, exporter, 5)

testing_label_set = meter.get_label_set({"environment": "testing"})

# Automatically collect standard metrics
auto_collection = AutoCollection(meter=meter, label_set=testing_label_set)

input("Press any key to exit...")
