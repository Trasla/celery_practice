import json
import pika
import smtplib
import ssl
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)
listen_error = sys.argv[1].lower()
errors = ['debug', 'info', 'warning', 'error']
print(' [*] Waiting for logs. To exit press CTRL+C'+listen_error)


def callback(ch, method, properties, body):
    total = json.loads(body)
    type_error = total['type'].replace("'", "").lower()
    body_message = total['body']
    asert = type_error in errors and listen_error == "debug"
    print(asert)
    if listen_error == "debug" and type_error in errors:
        file_write(type_error, body_message)
        emails(type_error, body_message)
        print(type_error)
        print(" [x] %r" % str(total['type']))
    elif listen_error == "info":
        file_write(type_error, body_message)
        emails(type_error, body_message)
        print(type_error)
        print(" [x] %r" % str(total['type']))
    elif listen_error == "warning":
        file_write(type_error, body_message)
        emails(type_error, body_message)
        print(type_error)
        print(" [x] %r" % str(total['type']))
    elif listen_error == "error" and type_error == listen_error:
        file_write(type_error, body_message)
        emails(type_error, body_message)
        print(type_error)
        print(" [x] %r" % str(total['type']))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()


def file_write(tip, total):
    f = open(tip + '.txt', '+a')
    f.write('Log = ' + tip + ': ' + total + '\n')
    f.close()


def emails(tip, total):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("PASS_EMAIL")
    message = 'Log = ' + tip + ': ' + total + '\n'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
