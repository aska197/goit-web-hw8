import pika
import json
from mongoengine import connect
from models import Contact

# Connect to MongoDB using the provided connection string
connect(
    db='contacts', 
    host='mongodb+srv://aska197:reira197@aska197.ayqixtn.mongodb.net/contacts?retryWrites=true&loadBalanced=false&replicaSet=atlas-ltn44s-shard-0&readPreference=primary&srvServiceName=mongodb&connectTimeoutMS=10000&w=majority&authSource=admin&authMechanism=SCRAM-SHA-1'
)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='email_queue')


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects.get(id=contact_id)
    # Simulate sending email (placeholder function)
    send_email(contact.email)
    # Update contact status to message sent
    contact.message_sent = True
    contact.save()
    print(f" [x] Email sent to {contact.email}")


def send_email(email):
    # Placeholder function to simulate sending email
    print(f"Sending email to {email}")


if __name__ == '__main__':
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue='email_queue',
                          on_message_callback=callback,
                          auto_ack=True)

    channel.start_consuming()

