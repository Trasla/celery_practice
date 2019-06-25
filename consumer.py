import pika
from time import sleep
from random import randint
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='test')


def callback(ch, method, properties, body):
    start_time = randint(1, 10)
    print(f'[x] recivied {body} y duermo por ', {start_time}, ' segundos')
    sleep(float(start_time))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test', on_message_callback=callback)

print('waiting for message...')
channel.start_consuming()
