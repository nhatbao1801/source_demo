import configparser
import requests
import requests
import json
from eventcenter.extra_settings.config import Config

configuration = Config()

def get_service_from_registry_service_by_dns(registry_host=str, registry_port=int, service_name=str):
    """Get service host by dns

    Args:
        registry_host (str, optional): Registry host. Defaults to str.
        registry_port (str, optional): registry port. Defaults to int.
        service_name (str, optional): service name. Defaults to str.

    Returns:
        _type_: _description_
    """
    if not registry_host or not registry_port:
        return None
    import subprocess
    import shlex
    cmd=f'dig @{registry_host} -p {registry_port} {service_name}.service.dc1.consul. ANY +short'
    print(cmd)
    proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
    out, err=proc.communicate()
    host = str(out).replace("b'","").split("\\n")[0]
    print(host)
    if len(host) <= 1:
        return None
    return host


def get_service_from_registry_service(service_name=None):
    consul_host = configuration.registry_host
    consul_port = configuration.registry_port
    consul_dns_port = configuration.registry_dns_port
    host = get_service_from_registry_service_by_dns(registry_host=consul_host, registry_port=consul_dns_port, service_name=service_name)
    url = f"http://{consul_host}:{consul_port}/v1/agent/service/{service_name}" 
    res = requests.get(url) 
    res = json.loads(res.text)
    return f"http://{host}:{res['Port']}"


# def get_profile_provider():
#     """Get profile provider

#     Returns:
#         provider_link: String provider link
#     """
#     profile_provider = configparser.ConfigParser()
#     profile_provider.read("provider.ini")
#     scheme = profile_provider.get("PROFILE_PROVIDER", "scheme")
#     host = profile_provider.get("PROFILE_PROVIDER", "host")
#     port = profile_provider.get("PROFILE_PROVIDER", "port")
#     return f'{scheme}://{host}:{port}'


def get_profile_provider():
    return get_service_from_registry_service(service_name="profile_service")

def get_form_provider():
    return get_service_from_registry_service(service_name="form_service")

def get_profile_list():
    _url = get_profile_provider()
    profile_response = requests.get(f"{_url}/profile").json()
    profile_list = profile_response.get('data')
    metadata = profile_response.get('metadata')
    return profile_list, metadata

def get_profile_detail(uid:str):
    _url = get_profile_provider()
    profile_info = requests.get(f"{_url}/profile/{uid}").json()
    return profile_info.get('data')

def get_business_level_code_detail(bl_code:str):
    _url = get_profile_provider()
    try:
        business_level_info = requests.get(f"{_url}/business_level_detail?business_level_id={bl_code}").json()
        return business_level_info.get('data').get('bl_code')
    except Exception as e:
        raise Exception(e)

def check_user_submited_form(target_id:str, uid:str):
    _url = get_form_provider()
    try:
        is_submited = requests.get(f"{_url}/form-submit-detail?target_id={target_id}&user_id={uid}&check_exists=True").json()
        return is_submited.get('data')
    except Exception as e:
        print("ERROR: ", e.__str__())
        return False