#!/usr/bin/env python
import pika
import json


def create_queue_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    return connection

def publish_message(connection, body):
    channel = connection.channel()
    request_queue =  channel.queue_declare(queue='code_request',  durable=True)
    response_queue = channel.queue_declare(queue='code_response',durable=True)
    channel.basic_publish(exchange='', routing_key='code_request', body=json.dumps(body))