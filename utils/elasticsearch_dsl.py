from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q, Bool, Match
from datetime import datetime, timedelta


class elasticsearch_base:
    request = ''
    s = ''
    result = ''
    my_Q = ''
    index = ''
    client = ''

    def __init__(self, host='127.0.0.1:9200', request_timeout=30, index='', request='', password=''):
        self.check_permission()

        if not password:
            self.client = Elasticsearch(host)
        else:
            self.client = Elasticsearch(host, http_auth='elastic:' + password, timeout=2, request_timeout=3,
                                        max_retries=0)

        self.s = Search(using=self.client, index=index)
        self.index = index

        if request:
            self.process_request(request)

    def get_raw(self):
        return self.s

    def match_phrase(self, field='', input=[]):
        if not field:
            return self

        if type(input) == str:
            input = [input]

        ######################
        ######################)
        exec('self.my_Q = Q("match_phrase", ' + field + '="' + input[0] + '")')
        for item in input[1:]:
            exec('self.my_Q |= Q("match_phrase", ' + field + '="' + item + '")')

        self.s = self.s.query(self.my_Q)

        return self

    def match_phrase_prefix(self, field='', input=[]):
        if not field:
            return self

        if type(input) == str:
            input = [input]

        ######################
        ######################)
        exec('self.my_Q = Q("match_phrase_prefix", ' + field + '="' + input[0] + '")')
        for item in input[1:]:
            exec('self.my_Q |= Q("match_phrase_prefix", ' + field + '="' + item + '")')

        self.s = self.s.query(self.my_Q)

        return self

    def match(self, field='', input=[]):
        if not field:
            return self

        if type(input) == str:
            input = [input]

        ######################
        ######################)
        exec('self.my_Q = Q("match", ' + field + '="' + input[0] + '")')
        for item in input[1:]:
            exec('self.my_Q |= Q("match", ' + field + '="' + item + '")')

        self.s = self.s.query(self.my_Q)

        return self

    def filter_in_range(self, field, m_range=[]):
        if not field or type(m_range) != list or len(m_range) < 2:
            print("ERROR!")
            return

        ######################
        ######################
        exec("self.s = self.s.filter('range', " + field + "={'gte': m_range[0], 'lte': m_range[1]})")

        return self

    def filter_in_time_range(self, field, last_num_of_days=3):
        start_date, end_date = self.get_last_day_range(days=last_num_of_days)

        self.filter_in_range(field, m_range=[start_date, end_date])

        return self

    def get_last_day_range(self, days=3):
        filtered_day_num = timedelta(days=days)
        start_date = (datetime.now() - filtered_day_num).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        return start_date, end_date

    def sort(self, input):
        self.s = self.s.sort(input)

        return self

    def source(self, field_list=[]):
        self.s = self.s.source(field_list)

        return self

    def exec(self, count=0):
        if not count:
            count = self.s.count()

        try:
            self.result = self.s[0:count].execute()
        except:
            print("CANNOT CONNECT ELASTICSEARCH .......")
            self.result = ''
            return self

        return self

    def json(self, start=0, end=-1):
        output = []

        if self.result:
            if self.result['hits']['hits']:
                if end == start:
                    return self.result['hits']['hits'][start]['_source'].__dict__['_d_']
                else:
                    for item in self.result['hits']['hits'][start:end + 1]:
                        output.append(item['_source'].__dict__['_d_'])

        return output

    def process_request(self):
        pass

    def check_permission(self):
        pass

    def get(self, field, value):
        exec("self.result = self.match_phrase(field='" + field + "',input='" + str(
            value) + "').source(['" + field + "']).exec(count=1).out()")
        return self.result

    def save(self, json):
        self.client.index(index=self.index, body=json)
        self.client.indices.refresh(index=self.index)

    def out(self):
        return self.result

    def query(self, field, input):
        if type(input) == list:
            input = input[0]

        exec("self.s = self.s.query(Match(" + field + "='" + input + "'))")
        return self

    def update(self, json):
        document_id = self.source(['ad_id']) \
            .exec(count=1).result['hits']['hits'][0]['_id']
