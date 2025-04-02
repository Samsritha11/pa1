from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import json

with open("data-am.json", "r") as file:
    data_am = json.load(file)
with open("data-nz.json", "r") as file:
    data_nz = json.load(file)
mergeddata = {**data_am, **data_nz}
with open("mergeddata.json", "w") as file: #mergeddata having two combined json files
    json.dump(mergeddata, file, indent=4)
    
master = SimpleXMLRPCServer(("localhost", 23000))
print("Master server listening on port 23000...")
worker1 = xmlrpc.client.ServerProxy("http://localhost:23001/")
worker2 = xmlrpc.client.ServerProxy("http://localhost:23002/")

def process_request(method, *args):
    if method == "getbylocation":
        return getbylocation(args[0])
    elif method == "getbyyear":
        return getbyyear(args[0], args[1])
    elif method == "getbyname":
        return getbyname(args[0])
    
def getbylocation(location):
    print("Merged data:", mergeddata)
    results = [item for item in mergeddata.values() if item.get("location") == location]
    return results

def getbyyear(location, year):
    results = [item for item in mergeddata.values() if item.get("location") == location and item.get("year") == year]
    return results

def getbyname(name):
    if name.lower()[0] in 'abcdefghijklm':
        return worker1.getbyname(name)
    elif name.lower()[0] in 'nopqrstuvwxyz':
        return worker2.getbyname(name)
    else:
        return "Invalid name"

master.register_function(process_request)
master.register_function(getbylocation, "getbylocation")
master.register_function(getbyyear, "getbyyear")
master.register_function(getbyname, "getbyname")
master.serve_forever()
