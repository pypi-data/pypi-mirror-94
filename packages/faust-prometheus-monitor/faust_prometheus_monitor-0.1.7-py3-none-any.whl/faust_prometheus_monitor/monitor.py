import re
from typing import Any, Dict, Optional, Pattern, cast

from aiohttp.web import Request, Response
from faust import web
from faust.sensors.monitor import Monitor, TPOffsetMapping
from faust.types import AppT, CollectionT, EventT, StreamT
from faust.types.assignor import PartitionAssignorT
from faust.types.topics import TopicT
from faust.types.transports import ConsumerT, ProducerT
from faust.types.tuples import Message, PendingMessage, RecordMetadata, TP
from prometheus_client import generate_latest, REGISTRY

from .metrics import (
    MESSAGE_IN,
    MESSAGE_OUT,
    STREAM_EVENT_IN,
    STREAM_EVENT_OUT,
    STREAM_EVENT_LATENCY,
    TOPIC_BUFFER_FULL,
    TABLE_OPS,
    COMMIT_LATENCY,
    SEND_INIT,
    SEND_HANDLED,
    SEND_LATENCY,
    TP_COMMIT,
    TP_END_OFFSET,
    TP_READ_OFFSET,
    ASSIGN_LATENCY,
    REBALANCE_TIME,
    REBALANCE_STATUS,
    WEB_REQUEST_STATUS,
    WEB_REQUEST_LATENCY,
)

# This regular expression is used to generate stream labels in Prometheus.
# It converts for example
#    'Stream: <Topic: withdrawals>'
# -> 'stream_topic_withdrawals'
#
# See PrometheusMonitor._normalize()
RE_NORMALIZE = re.compile(r"[\<\>:\s]+")
RE_NORMALIZE_SUBSTITUTION = "_"


def expose_metrics_http_response(request: Request) -> Response:
    headers = {"Content-Type": "text/plain; version=0.0.4; charset=utf-8"}
    return Response(body=generate_latest(REGISTRY), headers=headers, status=200)


class PrometheusMonitor(Monitor):
    """Prometheus Faust Sensor

    This sensor collects metrics and exposes them to a /metrics endpoint
    for Prometheus to scrape
    """

    def __init__(self, app_name: str, **kwargs) -> None:
        self.app_name = app_name
        super().__init__(**kwargs)

    def on_message_in(self, tp: TP, offset: int, message: Message) -> None:
        """Message received by a consumer."""
        super().on_message_in(tp, offset, message)
        MESSAGE_IN.labels(
            app=self.app_name, topic=tp.topic, partition=tp.partition
        ).inc()
        TP_READ_OFFSET.labels(
            app=self.app_name, topic=tp.topic, partition=tp.partition
        ).set(offset)

    def on_stream_event_in(
        self, tp: TP, offset: int, stream: StreamT, event: EventT
    ) -> Optional[Dict]:
        """Message sent to a stream as an event."""
        state = super().on_stream_event_in(tp, offset, stream, event)
        stream_label = (
            self._normalize(stream.shortlabel.lstrip("Stream:")).strip("_").lower()
        )
        STREAM_EVENT_IN.labels(
            app=self.app_name, topic=tp.topic, stream=stream_label
        ).inc()
        return state

    def on_stream_event_out(
        self, tp: TP, offset: int, stream: StreamT, event: EventT, state: Dict = None
    ) -> None:
        """Event was acknowledged by stream.
        Notes:
            Acknowledged means a stream finished processing the event, but
            given that multiple streams may be handling the same event,
            the message cannot be committed before all streams have
            processed it.  When all streams have acknowledged the event,
            it will go through :meth:`on_MESSAGE_OUT` just before offsets
            are committed.
        """
        super().on_stream_event_out(tp, offset, stream, event, state)
        stream_label = (
            self._normalize(stream.shortlabel.lstrip("Stream:")).strip("_").lower()
        )
        STREAM_EVENT_OUT.labels(
            app=self.app_name, topic=tp.topic, stream=stream_label
        ).inc()
        try:
            STREAM_EVENT_LATENCY.labels(
                app=self.app_name, topic=tp.topic, stream=stream_label
            ).observe(self.events_runtime[-1])
        except IndexError:
            STREAM_EVENT_LATENCY.labels(
                app=self.app_name, topic=tp.topic, stream=stream_label
            ).observe(self.secs_to_ms(0))

    def on_message_out(self, tp: TP, offset: int, message: Message) -> None:
        """All streams finished processing message."""
        super().on_message_out(tp, offset, message)
        MESSAGE_OUT.labels(
            app=self.app_name, topic=tp.topic, partition=tp.partition
        ).inc()

    def on_topic_buffer_full(self, topic: TopicT) -> None:
        """Topic buffer full so conductor had to wait."""
        super().on_topic_buffer_full(topic)
        TOPIC_BUFFER_FULL.labels(app=self.app_name, topic=topic).inc()

    def on_table_get(self, table: CollectionT, key: Any) -> None:
        """Key retrieved from table."""
        super().on_table_get(table, key)
        TABLE_OPS.labels(app=self.app_name, table=table.name, operation="get").inc()

    def on_table_set(self, table: CollectionT, key: Any, value: Any) -> None:
        """Value set for key in table."""
        super().on_table_set(table, key, value)
        TABLE_OPS.labels(app=self.app_name, table=table.name, operation="set").inc()

    def on_table_del(self, table: CollectionT, key: Any) -> None:
        """Key deleted from table."""
        super().on_table_del(table, key)
        TABLE_OPS.labels(app=self.app_name, table=table.name, operation="del").inc()

    def on_commit_completed(self, consumer: ConsumerT, state: Any) -> None:
        """Consumer finished committing topic offset."""
        super().on_commit_completed(consumer, state)
        COMMIT_LATENCY.labels(app=self.app_name).observe(
            self.secs_since(cast(float, state))
        )

    def on_send_initiated(
        self,
        producer: ProducerT,
        topic: str,
        message: PendingMessage,
        keysize: int,
        valsize: int,
    ) -> Any:
        """About to send a message."""
        SEND_INIT.labels(app=self.app_name, topic=topic).inc()
        return super().on_send_initiated(producer, topic, message, keysize, valsize)

    def on_send_completed(
        self, producer: ProducerT, state: Any, metadata: RecordMetadata
    ) -> None:
        """Message successfully sent."""
        super().on_send_completed(producer, state, metadata)
        SEND_LATENCY.labels(app=self.app_name).observe(
            self.secs_since(cast(float, state))
        )
        SEND_HANDLED.labels(app=self.app_name, status="success").inc()

    def on_send_error(
        self, producer: ProducerT, exc: BaseException, state: Any
    ) -> None:
        """Error while sending message."""
        super().on_send_error(producer, exc, state)
        SEND_HANDLED.labels(app=self.app_name, status="error").inc()

    def on_tp_commit(self, tp_offsets: TPOffsetMapping) -> None:
        """Call when offset in topic partition is committed."""
        super().on_tp_commit(tp_offsets)
        for tp, offset in tp_offsets.items():
            TP_COMMIT.labels(
                app=self.app_name, topic=tp.topic, partition=tp.partition
            ).set(offset)

    def track_tp_end_offset(self, tp: TP, offset: int) -> None:
        """Track new topic partition end offset for monitoring lags."""
        super().track_tp_end_offset(tp, offset)
        TP_END_OFFSET.labels(
            app=self.app_name, topic=tp.topic, partition=tp.partition
        ).set(offset)

    def on_assignment_error(
        self, assignor: PartitionAssignorT, state: Dict, exc: BaseException
    ) -> None:
        """Partition assignor did not complete assignor due to error."""
        super().on_assignment_error(assignor, state, exc)
        ASSIGN_LATENCY.labels(app=self.app_name, status="error").observe(
            self.secs_since(state["time_start"])
        )

    def on_assignment_completed(
        self, assignor: PartitionAssignorT, state: Dict
    ) -> None:
        """Partition assignor completed assignment."""
        super().on_assignment_completed(assignor, state)
        ASSIGN_LATENCY.labels(app=self.app_name, status="success").observe(
            self.secs_since(state["time_start"])
        )

    def on_rebalance_start(self, app: AppT) -> Dict:
        """Cluster rebalance in progress."""
        state = super().on_rebalance_start(app)
        REBALANCE_STATUS.labels(app=self.app_name).set(1)
        return state

    def on_rebalance_return(self, app: AppT, state: Dict) -> None:
        """Consumer replied assignment is done to broker."""
        super().on_rebalance_return(app, state)
        REBALANCE_TIME.labels(app=self.app_name, status="return").observe(
            self.secs_since(state["time_return"])
        )
        REBALANCE_STATUS.labels(app=self.app_name).set(2)

    def on_rebalance_end(self, app: AppT, state: Dict) -> None:
        """Cluster rebalance fully completed (including recovery)."""
        super().on_rebalance_end(app, state)
        REBALANCE_TIME.labels(app=self.app_name, status="recovering").observe(
            self.secs_since(state["time_return"])
        )
        REBALANCE_STATUS.labels(app=self.app_name).set(0)

    def on_web_request_end(
        self,
        app: AppT,
        request: web.Request,
        response: Optional[web.Response],
        state: Dict,
        *,
        view: web.View = None
    ) -> None:
        """Web server finished working on request."""
        super().on_web_request_end(app, request, response, state, view=view)
        if response is None:
            status_code = 500
        else:
            status_code = response.status
        WEB_REQUEST_STATUS.labels(app=self.app_name, status_code=status_code).inc()
        WEB_REQUEST_LATENCY.labels(app=self.app_name).observe(
            self.secs_since(state["time_end"])
        )

    def _normalize(
        self,
        name: str,
        *,
        pattern: Pattern = RE_NORMALIZE,
        substitution: str = RE_NORMALIZE_SUBSTITUTION
    ) -> str:
        return pattern.sub(substitution, name)
