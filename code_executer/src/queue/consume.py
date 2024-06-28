#!/usr/bin/env python
import pika
import json
from src.service.service import update_file, executer


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    request_queue = channel.queue_declare(queue='code_request',durable=True)
    response_queue = channel.queue_declare(queue='code_response',durable=True)


    def callback(ch, method, properties, body):
        body = json.loads(body)
        print(body)
        update_file(body['code'])
        output, container_id = executer(body['id_'])
        body_reponse = {"output":output, "id_": body["id_"], "container_id": container_id}
        channel.basic_publish(exchange='', routing_key='code_response', body=json.dumps(body_reponse))
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_consume(queue='code_request', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()