import pika
import json
from mongoengine import connect
from faker import Faker
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


def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            message_sent=False
            # Add other fields here if needed
        )
        contact.save()
        contacts.append(contact)
    return contacts


def send_contacts_to_queue(contacts):
    for contact in contacts:
        message = {
            'contact_id': str(contact.id)
        }
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=json.dumps(message))
        print(f" [x] Sent {message}")


if __name__ == '__main__':
    num_fake_contacts = 10
    fake_contacts = generate_fake_contacts(num_fake_contacts)
    send_contacts_to_queue(fake_contacts)
