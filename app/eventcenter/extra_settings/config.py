import os


class Config:
    port = os.getenv('SERVICE_PORT', 8010)
    address = os.getenv('SERVICE_ADDRESS' or 'event_service')
    registry_host = os.getenv('REGISTRY_HOST' or 'registry')
    registry_port = os.getenv('REGISTRY_PORT' or 8500)
    registry_dns_port = os.getenv('REGISTRY_DNS_PORT' or 8600)