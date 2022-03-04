#  Copyright (c) 2021
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

import os

ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', os.getenv('ELASTICSEARCH_HOST'))

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f'{ELASTICSEARCH_HOST}:9200' if ELASTICSEARCH_HOST else 'localhost:9200'
    },
}
