#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'in': 'header',
            'name': 'Authorization',
            'type': 'apiKey',
        },
    }
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': True
}
