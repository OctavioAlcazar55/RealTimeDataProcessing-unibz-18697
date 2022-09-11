#https://pypi.org/project/websocket_client/
import websocket
from confluent_kafka import Producer
import json
import datetime

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))

def json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise "Type %s not serializable" % type(obj)

def on_message(ws, message):
    
    message_json = json.loads(message)
    
    print(message_json.keys())
    if 'data' in message_json.keys() :
        print("Has Data!!!!!!!!!!!!!!!")
        for transaction in message_json["data"]:
            print("Has Transaction!!!!!!!!!!!!!!!")
            print(transaction)
            payload = json.dumps(transaction, default=json_serializer, ensure_ascii=False).encode('utf-8')
            producer.produce(topic='stock_events', key=str(transaction["s"]) + str(transaction["t"]), value=payload, callback=acked)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"META"}')
    ws.send('{"type":"subscribe","symbol":"MSFT"}')

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=ccdrikaad3i9bqco6u60",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()