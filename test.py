from prometheus_client import start_http_server, Summary, Counter, Gauge, Summary, CollectorRegistry, ProcessCollector
import random
import time

registry = CollectorRegistry()
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('srv_yammer_request_processing_seconds', 'Time spent processing request')
COUNTER = Counter('srv_yammer_my_failures_total', 'HTTP Failures', ['method', 'endpoint']).labels('get', '/')
GAUGE = Gauge('srv_yammer_my_inprogress_requests', 'Description of gauge')
SUMMARY = Summary('srv_yammer_request_latency_seconds', 'Description of summary')
PROCESS = ProcessCollector(proc='test', pid=lambda: open('/var/run/daemon.pid').read(), registry=registry)

# Decorate function with metric.
@REQUEST_TIME.time()
@COUNTER.count_exceptions()
@GAUGE.track_inprogress()
@SUMMARY.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)
    print(registry.get_sample_value('process_cpu_seconds_total'))


with COUNTER.count_exceptions():
    pass


with GAUGE.track_inprogress():
    pass


with SUMMARY.time():
    pass


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
