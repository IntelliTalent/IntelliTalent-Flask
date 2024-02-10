import os
import pika
import threading
from flask import Flask, jsonify
import json

app = Flask(__name__)


rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('RABBITMQ_COVER_LETTER_QUEUE')

def handle_command(command):
    if command == "healthCheck":
        return health_check()
    else:
        return {"error": "Unknown command"}

def listen_to_queue():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host,
                                                                   port=int(rabbitmq_port),
                                                                   virtual_host='/',
                                                                   credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)))
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    def callback(ch, method, properties, body):
        # This function will be called when a message is received
        # body variable contains the message data

        # Decode the message body
        message = json.loads(body.decode())

        pattern = message.get("pattern")

        # Extract the command from the message
        command = pattern.get("cmd")

        # Handle the command and get the response
        response = handle_command(command)

        # Get the reply_to queue from message properties
        reply_to = properties.reply_to

        ch.basic_publish(exchange='', routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response))


    # Start consuming messages
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


@app.route("/")
def main():
    return "Hello, World!"


@app.route('/healthCheck', methods=['GET'])
def health_check():
    return "Hello World From Cover Letter Service!"


if __name__ == "__main__":
    # Start listening to RabbitMQ in a separate thread
    rabbitmq_thread = threading.Thread(target=listen_to_queue)
    rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
    rabbitmq_thread.start()

    app.run(debug=True, threaded=True)
