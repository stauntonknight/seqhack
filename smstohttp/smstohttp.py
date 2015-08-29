import sys
import urllib

import requests
from Levenshtein import ratio
from specializations import specializations
from localities import localities

service_end_point = 'http://e2630397.ngrok.io/api/Services/GetServiceDetails/'
discovery_end_point = 'http://e2630397.ngrok.io/api/Services/GetApiDetails/'
keys = ['name', 'specialization']
service_list = {'practo': 'Practo'}
service_type_list = {'search': 'search'}
blacklist_words = set(["in", "from", "of"])

param_corpus_dict = {
    'speciality': specializations,
    'locality': localities
}


def leveinstein_match(key, tokens):
    for token in tokens:
        if ratio(key, token) > 0.90:
            return token


def make_request(service, service_type, params_dict):
    query_dict = {}
    query_dict['serviceName'] = service
    query_dict['apiName'] = service_type
    query_dict['parameters'] = urllib.urlencode(params_dict)
    resp = requests.get(service_end_point, params=query_dict)
    print params_dict
    return resp.json()


def get_first_matching(superset, tokens):
    for sl in superset:
        if sl in tokens:
            tokens.remove(sl)
            return sl
        else:
            match = leveinstein_match(sl, tokens)
            if match:
                tokens.remove(match)
                return sl


def main(sms):
    # sms formt CLIENT_CODE SERVICE PARAM1 PARAM2 ..
    print sms
    tokens = set(sms.lower().split())
    tokens = tokens.difference(blacklist_words)
    tokens = list(tokens)
    service = get_first_matching(service_list.keys(), tokens)
    if service is None:
        return ''
    service = service_list[service]
    service_type = get_first_matching(service_type_list.keys(), tokens)
    if service_type is None:
        return ''
    service_type = service_type_list[service_type]

    api_spec_req = requests.get(
        discovery_end_point,
        params={'serviceName': service, 'apiName': service_type})
    print api_spec_req.raw.read()
    print api_spec_req
    api_spec_req = api_spec_req.json()

    avail_params = {}
    for api_param in api_spec_req:
        if api_param in param_corpus_dict:
            avail_params[api_param] = get_first_matching(
                param_corpus_dict[api_param], tokens)

    if 'city' in api_spec_req:
        avail_params['city'] = 'Bangalore'

    if service is None or service_type is None:
        return ""

    resp = make_request(service, service_type, avail_params)
    return resp_to_text(resp)


def resp_to_text(resp):
    if 'doctors' not in resp:
        return ''
    resp = resp['doctors']
    keys = ['doctor_name', 'recommendation_percent', 'consultation_fees']
    resp_sms = ''
    for item in resp[:4]:
        for key in keys:
            if key in item:
                resp_sms += key + ": " + str(item[key])
                resp_sms += "\n"
        resp_sms += "\n"
    return resp_sms


if __name__ == '__main__':
    sys.argv[1]
    print main(sys.argv[1])
