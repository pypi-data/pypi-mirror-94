from prometheus_client import Counter, Gauge, Histogram


MESSAGE_IN = Counter(
    "faust_message_in",
    documentation="Message received by a consumer.",
    labelnames=["app", "topic", "partition"],
)
MESSAGE_OUT = Counter(
    "faust_message_out",
    documentation="All streams finished processing message.",
    labelnames=["app", "topic", "partition"],
)
STREAM_EVENT_IN = Counter(
    "faust_stream_event_in",
    documentation="Message sent to a stream as an event.",
    labelnames=["app", "topic", "stream"],
)
STREAM_EVENT_OUT = Counter(
    "faust_stream_event_out",
    documentation="Event was acknowledged by stream.",
    labelnames=["app", "topic", "stream"],
)
STREAM_EVENT_LATENCY = Histogram(
    "faust_stream_event_latency",
    documentation="How long the event took to process.",
    labelnames=["app", "topic", "stream"],
)
TOPIC_BUFFER_FULL = Counter(
    "faust_topic_buffer_full",
    documentation="Topic buffer full so conductor had to wait.",
    labelnames=["app", "topic"],
)
TABLE_OPS = Counter(
    "faust_table_operations",
    documentation="Operations of faust tables (get, set, delete)",
    labelnames=["app", "table", "operation"],
)
COMMIT_LATENCY = Histogram(
    "faust_commit_latency",
    documentation="Latency of consumer committing topic offset.",
    labelnames=["app"],
)
SEND_INIT = Counter(
    "faust_send_initialized",
    documentation="About to send a message.",
    labelnames=["app", "topic"],
)
SEND_HANDLED = Counter(
    "faust_send_handled",
    documentation="Total number of messages sent regardless of success or failure",
    labelnames=["app", "status"],
)
SEND_LATENCY = Histogram(
    "faust_send_latency",
    documentation="Latency of sending messages",
    labelnames=["app"],
)
TP_COMMIT = Gauge(
    "faust_topic_commit",
    documentation="Gauge for what offset in topic partition is committed.",
    labelnames=["app", "topic", "partition"],
)
TP_END_OFFSET = Gauge(
    "faust_topic_end_offset",
    documentation="Track new topic partition end offset for monitoring lags.",
    labelnames=["app", "topic", "partition"],
)
TP_READ_OFFSET = Gauge(
    "faust_topic_read_offset",
    documentation="Topic partition read offset that consumer is on.",
    labelnames=["app", "topic", "partition"],
)
ASSIGN_LATENCY = Histogram(
    "faust_assignment_latency",
    documentation="Partition assignor completion latency regardless success or error",
    labelnames=["app", "status"],
)
REBALANCE_TIME = Histogram(
    "faust_rebalance_time",
    documentation="Cluster rebalance latency.",
    labelnames=["app", "status"],
)
REBALANCE_STATUS = Gauge(
    "faust_rebalance_status",
    documentation="Cluster rebalance status. "
    "0: rebalance fully completed (including recovery); "
    "1: rebalance started; "
    "2: Consumer replied assignment is done to broker",
    labelnames=["app"],
)
WEB_REQUEST_STATUS = Counter(
    "faust_web_request_status_codes",
    documentation="Status code counters on faust web views",
    labelnames=["app", "status_code"],
)
WEB_REQUEST_LATENCY = Histogram(
    "faust_web_request_latency",
    documentation="Request latency on faust web views",
    labelnames=["app"],
)
