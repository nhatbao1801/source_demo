import requests
import json

from eventcenter.extra_settings.config import Config


configuration = Config()

def register_to_registry_service():
    url = f"http://{configuration.registry_host}:{configuration.registry_port}/v1/agent/service/register"
    data = {
        "Name": "event_service",
        "Tags": ["event_service"],
        "Address": configuration.address,
        'Port': int(configuration.port),
        "Check": {
            "http": f"http://{configuration.address}:{configuration.port}/health",
            "interval": "10s"
        }
    }
    print("Service registration parameters: ", data)
    res = {"message": "registering"}
    res = requests.put(url, data=json.dumps(data))
    return res.text