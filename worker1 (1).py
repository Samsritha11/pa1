from xmlrpc.server import SimpleXMLRPCServer
import json

receiveddata = None
def PublishData(data):
    print("Worker 1: Received data from publisher:", data)
    global receiveddata
    receiveddata = data
    
with open("mergeddata.json", "r") as file:
    mergeddata = json.load(file)

worker1 = SimpleXMLRPCServer(("localhost", 23001), allow_none=True)
def getbylocation(location):
    results = [item for item in mergeddata if item.get("location") == location]
    return results
def getbyyear(location, year):
    results = [item for item in mergeddata.values() if item.get("location") == location and item.get("year") == year]
    return results
def getbyname(name):
    if name.lower()[0] in 'abcdefghijklm':
        for item in mergeddata.values():
            if item.get("name") == name:
                return f"Worker 1: Processing request for name '{name}'"
        return f"Worker 1: No record found for name '{name}'"
    else:
        return "Worker 1: Name not handled"
worker1.register_function(getbylocation, "getbylocation")
worker1.register_function(getbyyear, "getbyyear")
worker1.register_function(getbyname, "getbyname")
worker1.register_function(PublishData, "PublishData")
print("Worker server listening on port 23001...")
worker1.serve_forever()
