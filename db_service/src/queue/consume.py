#!/usr/bin/env python
import pika
import json
from src.service.db import add_response_into_db,initialize_redis_connection




def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    redis_connection = initialize_redis_connection()

    request_queue = channel.queue_declare(queue='code_request',durable=True)
    response_queue = channel.queue_declare(queue='code_response',durable=True)


    def callback(ch, method, properties, body):
        body = json.loads(body)
        print(body)
        add_response_into_db(redis_connection,body['id_'],body['output'])
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_consume(queue='code_response', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()