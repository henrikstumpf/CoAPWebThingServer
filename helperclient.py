from coapthon.client.helperclient import HelperClient
import json

client = HelperClient(server=("192.168.71.34", 5684))
response = client.get("things/Sensor1")
if response.content_type == 0:
    #STRING
    data = response.payload
elif response.content_type == 50:
    #JSON
    data = json.loads(response.payload)
else:
    pass

print(data)

thing_api = data
for property_name, metadata in thing_api['properties'].items():
    print(metadata)

client.stop()
