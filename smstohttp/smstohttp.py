import sys

import requests

service_end_point = 'http://b0a68fa7.ngrok.io/api/Services/getservice'
discovery_end_point = 'http://b0a68fa7.ngrok.io/api/Services/GetApiDetails'


def make_request(client_code, call_name, query_params, api_spec):
    """
    api_spec = [param1, param2, param3]
    """
    return [{
        'name': 'B.Kappur',
        'specilization': 'Neurology'
    }]
    params_dict = dict(zip(api_spec, query_params))
    params_dict['serviceId'] = client_code
    params_dict['serviceName'] = call_name
    resp = requests.get(service_end_point, params=params_dict)
    return resp.json()


def main(sms):
    # sms formt CLIENT_CODE SERVICE PARAM1 PARAM2 ..
    query_params = sms.split()
    client_code, call_name, query_params = (query_params[0], query_params[1],
                                            query_params[2:])
    # api_spec = requests.get(
    #     discovery_end_point,
    #     params={'serviceId': client_code, 'serviceName': call_name})
    api_spec = []

    resp = make_request(client_code, call_name, query_params, api_spec)
    keys = ['name', 'specilization']
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
