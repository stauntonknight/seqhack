import sys

import requests
from Levenshtein import ratio
from specializations import specialization

service_end_point = 'http://b0a68fa7.ngrok.io/api/Services/getservice'
discovery_end_point = 'http://b0a68fa7.ngrok.io/api/Services/GetApiDetails'
keys = ['name', 'specilization']
service_list = ["practo"]
service_type_list = ["get_doctors"]
blacklist_words = set(["in", "from", "of"])


def leveinstein_match(key, tokens):
    for token in tokens:
        if ratio(key, token) > 0.90:
            return token


def make_request(service, service_type, params_dict):
    return [{
        'name': 'B.Kappur',
        'specilization': 'Neurology'
    }]
    params_dict['serviceId'] = service
    params_dict['serviceName'] = service_type
    resp = requests.get(service_end_point, params=params_dict)
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
    tokens = set(sms.lower().split())
    tokens = tokens.difference(blacklist_words)
    service = get_first_matching(service_list, tokens)
    service_type = get_first_matching(service_type_list, tokens)

    # api_spec_req = requests.get(
    #     discovery_end_point,
    #     params={'serviceId': client_code, 'serviceName': call_name})
    api_spec_req = ['specialization']  # remove this line

    avail_params = {}
    for api_param in api_spec_req:
        avail_params[api_param] = get_first_matching(globals()[api_param],
                                                     tokens)

    if service is None or service_type is None:
        return ""
    tokens = list(tokens)

    for req_param in api_spec_req:
        if req_param not in avail_params:
            return ""
    resp = make_request(service, service_type, avail_params)
    print avail_params
    return resp_to_text(resp)


def resp_to_text(resp):
    for item in resp:
        resp_sms = ''
        for key in keys:
            if key in item:
                resp_sms += key + ": " + str(item[key])
                resp_sms += "\n"
        resp_sms += "\n"
    return resp_sms


if __name__ == '__main__':
    sys.argv[1]
    print main(sys.argv[1])
