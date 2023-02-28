
import requests
import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)


#parameters = pika.URLParameters('amqp://geust:geust@localhost:5672/%2F')

def on_request(channel, method, props, body):
    # Handle the incoming message here
    print(body)
    headers = {'Content-Type': 'application/json'}
    res = requests.get('http://127.0.0.1:6000/notify')

    response = "Response Message"
    channel.basic_publish(exchange='',
                          routing_key=str(props.reply_to),
                          properties=pika.BasicProperties(correlation_id = props.correlation_id),
                          body=str(response))
    channel.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='my_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='my_queue', on_message_callback=on_request)

print("RPC server is running...")
channel.start_consuming()





