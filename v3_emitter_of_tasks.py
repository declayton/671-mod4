"""
    This program sends a message to a queue on the RabbitMQ server.
    Make tasks harder/longer-running by adding dots at the end of the message.

    Author: Deanna Clayton
    Date: February 6, 2023

"""

import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# read from a file to get some data
input_file = open("tasks.csv", "r")

# create a csv reader for our comma delimited data
reader = csv.reader(input_file, delimiter=",")

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    show_offer = False
    if show_offer == True:
        offer_rabbitmq_admin_site()
    
    for row in reader:
        # read a row from the file
        Task = row
        # get the message from the command line
        # if no arguments are provided, use the default message
        # use the join method to convert the list of arguments into a string
        # join by the space character inside the quotes
        message = " ".join(sys.argv[1:]) or f"{Task}"
        # send the message to the queue
        send_message("localhost","task_queue3",message)
        # tell the user the message was sent
        print(f" [x] Sent {message}")
        # sleep for a second
        time.sleep(3)


    



