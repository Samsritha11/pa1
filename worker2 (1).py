from xmlrpc.server import SimpleXMLRPCServer
import json

with open("mergeddata.json", "r") as file:
    mergeddata = json.load(file)

worker2 = SimpleXMLRPCServer(("localhost", 23002), allow_none=True)

def getbylocation(location):
    results = [item for item in mergeddata if item.get("location") == location]
    return results
def getbyyear(location, year):
    results = [item for item in mergeddata.values() if item.get("location") == location and item.get("year") == year]
    return results
def getbyname(name):
    if name.lower()[0] in 'nopqrstuvwxyz':
        for item in mergeddata.values():
            if item.get("name") == name:
                return f"Worker 2: Processing request for name '{name}'"
        return f"Worker 2: No record found for name '{name}'"
    else:
        return "Worker 2: Name not handled"
def PublishData(data):
    print("Worker 2: Received data from publisher:", data)

worker2.register_function(getbylocation, "getbylocation")
worker2.register_function(getbyyear, "getbyyear")
worker2.register_function(getbyname, "getbyname")
worker2.register_function(PublishData, "PublishData")
print("Worker server listening on port 23002...")
worker2.serve_forever()
