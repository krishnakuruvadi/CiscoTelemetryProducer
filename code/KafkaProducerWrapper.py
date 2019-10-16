"""Kafka wrapper for easy interface with protobufs and sending on channels bound
to that schema"""
"""https://github.com/brynmathias/MessageCorps/blob/master/MessageCorps/broker.py"""

import logging
import os
import sys
import threading
from time import sleep, time

from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from tenacity import retry, stop_after_attempt, wait_exponential

from .pb_handler import MessageHandler

LOGGER = logging.getLogger(__name__)


class MessagingException(Exception):
    """Exception type for messaging"""
    pass


class MessagingExceptionCritical(MessagingException):
    def __init__(self, e):
        super().__init__()
        sys.exit(0)


class KafkaProducerWrapper(object):
    """docstring for KafkaProducer"""

    def __init__(self, topic=None, bootstrap_servers=None, async=True, **kwargs):
        super(KafkaProducerWrapper, self).__init__()
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers if isinstance(
            bootstrap_servers, list) else [bootstrap_servers, ]
        self.async = async
        self.producer = None
        self.producer_args = kwargs
        self.setup()

    def setup(self):
        try:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
            LOGGER.debug(f"Setting producer topic to {self.topic}")
        except Exception as e:
            LOGGER.fatal("Could not create kafka producer",
                         exc_info=True)
            raise e

    def send(self, pb, topic=None, callback=None):
        """docstring for send"""
        this_topic = None
        message = None
        LOGGER.debug(f"called to send {pb}, self.topic {self.topic}, topic {topic}")
        if self.topic:
            this_topic = self.topic
            message = MessageHandler(pb)
        elif topic:
            this_topic = topic
            message = MessageHandler(pb)
        else:
            raise MessagingException("Called send without a topic and producer " +
                                     f"instantiated with topic = None {self.topic}")
        self.producer.send(this_topic, message.compress())
        if callable(callback):
            callback()

