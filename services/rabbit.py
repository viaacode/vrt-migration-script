#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pika
from pika.credentials import PlainCredentials
import time


class RabbitService(object):
    def __init__(self, config: dict):
        self.credentials = pika.PlainCredentials(
            config["rabbit"]["user"], config["rabbit"]["password"]
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config["rabbit"]["host"],
                port=config["rabbit"]["port"],
                credentials=self.credentials,
            )
        )

        self.channel = self.connection.channel()
        self.exchange = config["rabbit"]["exchange"]
        self.routing_key = config["rabbit"]["routing_key"]

    def publish_message(self, message: str) -> bool:
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=message,
            )

            return True

        except pika.exceptions.AMQPConnectionError as ce:
            raise ce
