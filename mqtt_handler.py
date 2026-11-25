import paho.mqtt.client as mqtt

def create_client(broker, port, topic, callback):
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect=lambda c,u,f,rc: c.subscribe(topic)
    client.on_message=callback
    client.connect(broker, port, 60)
    return client
