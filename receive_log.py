import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
result_queue = channel.queue_declare(queue='', exclusive=True)
queue_name = result_queue.method.queue
channel.queue_bin(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    print(f'[x] received {body}')


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Starting consuming...')
channel.start_consumming()