import xmlrpc.client
import json

try:
    master_proxy = xmlrpc.client.ServerProxy("http://localhost:23000/")
    location = 'City'
    print(f'Client => Asking for person lived at {location}')
    result = master_proxy.getbylocation(location)
    print(result)
    print()

    location = 'New York City'
    year = 2002
    print(f'Client => Asking for person lived in {location} in {year}')
    result = master_proxy.getbyyear(location, year)
    print(result)
    print()

    name = 'xu'
    print(f'Client => Asking for person with {name}')
    result = master_proxy.getbyname(name)
    if "No record found" in result:
        print(f"No record found for {name}.")
    else:
        print(result)
    print()

except ConnectionRefusedError:
    print("Error: Connection refused. Server may be unavailable.")
except Exception as e:
    print(f"Error: {e}")
