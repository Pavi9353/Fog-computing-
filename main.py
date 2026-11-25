import json, os, time, sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "campus/sensors"
DB = os.getenv("DB_PATH", "fog_data.db")

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS readings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, device_id TEXT, temperature REAL,
            humidity REAL, occupancy INTEGER, air_quality INTEGER,
            status TEXT, action TEXT)""")

def process(data):
    alerts=[]
    actions=[]
    t=float(data.get("temperature",0))
    h=float(data.get("humidity",0))
    aq=int(data.get("air_quality",0))
    occ=int(data.get("occupancy",0))

    if t > 30: alerts.append("HIGH_TEMPERATURE"); actions.append("VENTILATION_ON")
    if aq > 700: alerts.append("POOR_AIR_QUALITY"); actions.append("ALARM_ON")
    if occ == 1: alerts.append("MOTION_DETECTED")

    status="ALERT" if alerts else "NORMAL"
    return status, ",".join(alerts) or "NONE", ",".join(actions) or "NONE"

def on_connect(client, userdata, flags, rc):
    print("Fog node connected to MQTT:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        data=json.loads(msg.payload.decode())
        status, alerts, actions=process(data)
        now=datetime.now().isoformat(timespec="seconds")
        with sqlite3.connect(DB) as con:
            con.execute("""INSERT INTO readings
                (timestamp,device_id,temperature,humidity,occupancy,air_quality,status,action)
                VALUES(?,?,?,?,?,?,?,?)""",
                (now,data.get("device_id","unknown"),data.get("temperature"),
                 data.get("humidity"),data.get("occupancy"),data.get("air_quality"),
                 status,actions))
        print(f"[{now}] {status} | alerts={alerts} | actions={actions}")
    except Exception as e:
        print("Invalid message:", e)

if __name__ == "__main__":
    init_db()
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect=on_connect
    client.on_message=on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Fog processing node started...")
    client.loop_forever()
