# iot.io Client
### iot.io Overview
This project aims to create a lightweight and intuitive system for connecting
IoT devices to a central server for small IoT system implementations and hobbyists.

The framework focuses on providing easy to use system of libraries so the end user does
not need to understand the protocol implementation, though this also is fairly simple.

The format of the framework is somewhat reminiscent of [Socket.IO](https://socket.io/) 
where handlers functions are defined and executed and run as events are triggered.


### Quickstart Guide (Client)
This is an example of a simple IoTClient instance which connects to a server accepting
"echo" clients ping the server every 5 seconds with a message and print the server's response.

```python
from iotio_client import IoTClient
import threading
import time

# create client
client = IoTClient("echo_test_client", "echo")


# define a handler for "echo_response" events
@client.on("echo_response")
def echo(data):
    print("'echo_response' from Server: '" + str(data) + "'\n")


def send():
    client.ensure_open()

    # loop while client is connected
    while client.connected:
        message = input("Enter a value to send to the server: ")

        # send message over the echo channel
        client.send("echo", message)
        print("")
        time.sleep(1)


# start background send task
send_thread = threading.Thread(None, send)
send_thread.start()

# connect client
client.run("localhost:5000", use_tls=False)
send_thread.join()
```

If you would like to see the matching quick-start guide for an example
server go [here](https://github.com/dylancrockett/iot.io).

