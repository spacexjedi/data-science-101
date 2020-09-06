import paho.mqtt.client as mqtt
#import context
import paho.mqtt.subscribe as subscribe

topics = ['tnt']
user = ''
pwd = ''

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
#username_pw_set(user, password=pwd)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("tnt-iot.maratona.dev", 30573, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

m = subscribe.simple(topics, hostname="tnt-iot.maratona.dev", port=30573, retained=False, msg_count=2, auth = {‘username’:”<username>”, ‘password’:”<password>”})
for a in m:
    print(a.topic)
    print(a.payload)

client.loop_forever()