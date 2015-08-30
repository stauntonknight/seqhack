import sys
import urllib

import requests
from Levenshtein import ratio
from specializations import specializations
from localities import localities
from google_types import google_types

service_end_point = 'http://f644da1e.ngrok.io/api/Services/GetServiceDetails/'
discovery_end_point = 'http://f644da1e.ngrok.io/api/Services/GetApiDetails/'
keys = ['name', 'specialization']
service_list = {'practo': 'Practo', 'google': 'Google'}
service_type_list = {'search': 'search', 'near': 'nearbySearch'}
blacklist_words = set(["in", "from", "of"])

param_corpus_dict = {
    'speciality': specializations,
    'locality': localities,
    'location': localities,
    'types': google_types
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
    print service
    print service_type

    api_spec_req = requests.get(
        discovery_end_point,
        params={'serviceName': service, 'apiName': service_type})
    print api_spec_req.raw.read()
    print api_spec_req
    api_spec_req = api_spec_req.json()

    avail_params = {}
    # api_spec_req = ['location', 'radius', 'types']
    for api_param in api_spec_req:
        if api_param in param_corpus_dict:
            if api_param == 'location':
                loca = get_first_matching(param_corpus_dict[api_param], tokens)
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyDQT4UfphqtqYYYxGRsUjChUK6GeUDmLfY' % loca
                lat_lng = requests.get(url).json()['results'][0]
                location = lat_lng['geometry'][u'location']
                avail_params[api_param] = str(location['lat']) + ',' + str(location['lng'])
            else:
                avail_params[api_param] = get_first_matching(
                    param_corpus_dict[api_param], tokens)
                print api_param
                print get_first_matching(
                    param_corpus_dict[api_param], tokens)
    if 'radius' in api_spec_req:
        avail_params['radius'] = 500

    if 'city' in api_spec_req:
        avail_params['city'] = 'Bangalore'

    print avail_params
    print api_spec_req

    if service is None or service_type is None:
        return ""

    resp = make_request(service, service_type, avail_params)
    return resp_to_text(resp, service)


def resp_to_text(resp, service):
    if service=='Practo':
        if 'doctors' not in resp:
            return ''
        resp = resp['doctors']
    elif service=='Google':
        resp = resp['results']
    else:
        return ''

    keys = ['doctor_name', 'recommendation_percent', 'consultation_fees', 'name', 'rating', 'vicinity']
    resp_sms = ''
    for item in resp[:3]:
        for key in keys:
            if key in item:
                resp_sms += key.replace('_', ' ').title() + ": " + str(item[key])
                resp_sms += "\n"
        resp_sms += "\n"
    return resp_sms


if __name__ == '__main__':
    sys.argv[1]
    print main(sys.argv[1])
