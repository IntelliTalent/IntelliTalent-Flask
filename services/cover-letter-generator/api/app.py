from flask import (
    Flask,
    jsonify,
)
from .index import (
    main,
)
from .logger import (
    logger
)
import os, pika, threading, json

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
# for each service, the queue name should be unique
rabbitmq_queue = os.getenv('')

def create_app():
    app = Flask(__name__)
    
    # Start listening to RabbitMQ in a separate thread
    rabbitmq_thread = threading.Thread(target=listen_to_queue)
    rabbitmq_thread.daemon = True  # Stop the thread when the main thread exits
    rabbitmq_thread.start()

    # doesn't do anything
    app.route("/", methods=["GET"])(main)
    
    # health check, replica of healthCheck pattern
    app.route("/healthCheck", methods=["GET"])(health_check)

    return app

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
        # body variable contains RABBITMQ_COVER_LETTER_QUEUE message data

        # Decode the message body
        message = json.loads(body.decode())
 
        pattern = message.get("pattern")

        # Extract the command from the message
        command = pattern.get("cmd")

        # Handle the command and get the response
        response = handle_command(command)

        # Get the reply_to queue from message properties
        reply_to = properties.reply_to

        ch.basic_publish(exchange='', routing_key=reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response))


    # Start consuming messages
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()
    
def health_check():
    return "Hello World From Cover Letter Service!"
