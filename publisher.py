import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='test')
for i in range(1, 11):
    body = str(i)
    channel.basic_publish(exchange='', routing_key='test', body=body)
    print('[x] Sent')
connection.close()
