# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import mock
import time
import unittest

from azure_monitor.trace import AzureMonitorSpanExporter

class TestAzureExporter(unittest.TestCase):
    def test_ctor(self):
        from azure_monitor.utils import Options
        instrumentation_key = Options._default.instrumentation_key
        Options._default.instrumentation_key = None
        self.assertRaises(ValueError, lambda: AzureMonitorSpanExporter())
        Options._default.instrumentation_key = instrumentation_key

    def test_span_data_to_envelope(self):
        from opentelemetry.trace import SpanKind
        from opentelemetry.sdk.trace import Span
        from opentelemetry.trace import SpanContext

        exporter = AzureMonitorSpanExporter(
            instrumentation_key='12345678-1234-5678-abcd-12345678abcd'
        )

        parent_span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557338,
            ),
        )

        start_time = 1575494316027612800
        end_time = start_time + 1001000000

        # SpanKind.CLIENT HTTP
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=parent_span,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={
                'component': 'http',
                'http.method': 'GET',
                'http.url': 'https://www.wikipedia.org/wiki/Rabbit',
                'http.status_code': 200,
            },
            events=None,
            links=None,
            kind=SpanKind.CLIENT
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.RemoteDependency')
        self.assertEqual(
            envelope.tags['ai.operation.parentId'],
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31da.')
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.name,
            'GET//wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseData.data,
            'https://www.wikipedia.org/wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseData.target,
            'www.wikipedia.org')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.resultCode,
            '200')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseData.type,
            'HTTP')
        self.assertEqual(
            envelope.data.baseType,
            'RemoteDependencyData')

        # SpanKind.CLIENT unknown type
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=parent_span,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={},
            events=None,
            links=None,
            kind=SpanKind.CLIENT
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.RemoteDependency')
        self.assertEqual(
            envelope.tags['ai.operation.parentId'],
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31da.')
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.name,
            'test')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseData.type,
            None)
        self.assertEqual(
            envelope.data.baseType,
            'RemoteDependencyData')

        # SpanKind.CLIENT missing method
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=parent_span,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={
                'component': 'http',
                'http.url': 'https://www.wikipedia.org/wiki/Rabbit',
                'http.status_code': 200,
            },
            events=None,
            links=None,
            kind=SpanKind.CLIENT
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.RemoteDependency')
        self.assertEqual(
            envelope.tags['ai.operation.parentId'],
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31da.')
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.name,
            'test')
        self.assertEqual(
            envelope.data.baseData.data,
            'https://www.wikipedia.org/wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseData.target,
            'www.wikipedia.org')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.resultCode,
            '200')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseData.type,
            'HTTP')
        self.assertEqual(
            envelope.data.baseType,
            'RemoteDependencyData')

        # SpanKind.SERVER HTTP - 200 request
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=parent_span,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={
                'component': 'http',
                'http.method': 'GET',
                'http.path': '/wiki/Rabbit',
                'http.route': '/wiki/Rabbit',
                'http.url': 'https://www.wikipedia.org/wiki/Rabbit',
                'http.status_code': 200,
            },
            events=None,
            links=None,
            kind=SpanKind.SERVER
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.Request')
        self.assertEqual(
            envelope.tags['ai.operation.parentId'],
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31da.')
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.tags['ai.operation.name'],
            'GET /wiki/Rabbit')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseData.responseCode,
            '200')
        self.assertEqual(
            envelope.data.baseData.name,
            'GET /wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseData.success,
            True)
        self.assertEqual(
            envelope.data.baseData.url,
            'https://www.wikipedia.org/wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseType,
            'RequestData')

        # SpanKind.SERVER HTTP - Failed request
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=parent_span,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={
                'component': 'http',
                'http.method': 'GET',
                'http.path': '/wiki/Rabbit',
                'http.route': '/wiki/Rabbit',
                'http.url': 'https://www.wikipedia.org/wiki/Rabbit',
                'http.status_code': 400,
            },
            events=None,
            links=None,
            kind=SpanKind.SERVER
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.Request')
        self.assertEqual(
            envelope.tags['ai.operation.parentId'],
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31da.')
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.tags['ai.operation.name'],
            'GET /wiki/Rabbit')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseData.responseCode,
            '400')
        self.assertEqual(
            envelope.data.baseData.name,
            'GET /wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseData.success,
            False)
        self.assertEqual(
            envelope.data.baseData.url,
            'https://www.wikipedia.org/wiki/Rabbit')
        self.assertEqual(
            envelope.data.baseType,
            'RequestData')

        # SpanKind.SERVER unknown type
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=parent_span,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={
                'component': 'http',
                'http.method': 'GET',
                'http.path': '/wiki/Rabbit',
                'http.route': '/wiki/Rabbit',
                'http.url': 'https://www.wikipedia.org/wiki/Rabbit',
                'http.status_code': 400,
            },
            events=None,
            links=None,
            kind=SpanKind.SERVER
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.Request')
        self.assertEqual(
            envelope.tags['ai.operation.parentId'],
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31da.')
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseType,
            'RequestData')

        # SpanKind.INTERNAL
        span = Span(
            name='test',
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557337,
            ),
            parent=None,
            sampler=None,
            trace_config=None,
            resource=None,
            attributes={'key1': 'value1'},
            events=None,
            links=None,
            kind=SpanKind.INTERNAL
        )
        span.start_time = start_time
        span.end_time = end_time
        envelope = exporter.span_to_envelope(span)
        self.assertEqual(
            envelope.iKey,
            '12345678-1234-5678-abcd-12345678abcd')
        self.assertEqual(
            envelope.name,
            'Microsoft.ApplicationInsights.RemoteDependency')
        self.assertRaises(
            KeyError,
            lambda: envelope.tags['ai.operation.parentId'])
        self.assertEqual(
            envelope.tags['ai.operation.id'],
            '1bbd944a73a05d89eab5d3740a213ee7')
        self.assertEqual(
            envelope.time,
            '2019-12-04T21:18:36.027613Z')
        self.assertEqual(
            envelope.data.baseData.name,
            'test')
        self.assertEqual(
            envelope.data.baseData.duration,
            '0.00:00:01.001')
        self.assertEqual(
            envelope.data.baseData.id,
            '|1bbd944a73a05d89eab5d3740a213ee7.a6f5d48acb4d31d9.')
        self.assertEqual(
            envelope.data.baseData.type,
            'InProc')
        self.assertEqual(
            envelope.data.baseType,
            'RemoteDependencyData')
