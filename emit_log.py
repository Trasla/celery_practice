import pika
import sys
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
if len(sys.argv) > 2:
    type_error = (sys.argv[1]).lower()
    body = ' '.join(sys.argv[2:])
    message = json.dumps({'type': type_error, 'body': body})
else:
    message = json.dumps({'type': 'info', 'body': 'hello'})
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()
