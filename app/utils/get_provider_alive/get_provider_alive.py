import configparser

import requests


def get_profile_provider():
    """Get profile provider

    Returns:
        provider_link: String provider link
    """
    profile_provider = configparser.ConfigParser()
    profile_provider.read("provider.ini")
    scheme = profile_provider.get("PROFILE_PROVIDER", "scheme")
    host = profile_provider.get("PROFILE_PROVIDER", "host")
    port = profile_provider.get("PROFILE_PROVIDER", "port")
    return f'{scheme}://{host}:{port}'


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