An HTTP server for reading and storing simple values.
Each item will be stored in a list so you can add multiple items to the same key as well as remove just single items from a key list.

Basically, this is an HTTP frontend to redis.

The server is started using TornRPC (https://github.com/sk8erwitskil/TornRPC) but you can make HTTP calls to the server as well.
```
curl -H "User-Agent: TornRPC" -X GET -d "key=kyle" http://my_ip.address.com:80/get
curl -H "User-Agent: TornRPC" -X GET -d "key=kyle&val=owner" http://my_ip.address.com:80/add
```
The response will be a JSON object like ```{"response": ["owner"]}```. The value here is to not require needing a redis library to interact with the server.


### Dependencies ###
- tornado
- redis
- TornRPC

### Example ###
First start the server.
```
python server.py --port=80 --redis=127.0.0.1:6379
```

Then in a different location simply
```python
from tornrpc.client import TornRPCClient
client = TornRPCClient("my_ip.address.com:80")
print client.add("github", "https://github.com/sk8erwitskil")
print client.add("github", "https://github.com/sk8erwitskil/TornRPC")
for item in client.get("github"):
  print item
```
