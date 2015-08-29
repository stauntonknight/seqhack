import sys
import requests
import specializations

service_end_point = 'http://b0a68fa7.ngrok.io/api/Services/getservice'
discovery_end_point = 'http://b0a68fa7.ngrok.io/api/Services/GetApiDetails'
keys = ['name', 'specilization']
service_list = ["practo"]
service_type_list = ["get_doctors"]
blacklist_words = set(["in", "from", "of"])


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


def get_first_matching(superset, param):
    slist = None
    for sl in superset:
        if (sl in param):
            slist = sl
            break
    return slist

def main(sms):
    # sms formt CLIENT_CODE SERVICE PARAM1 PARAM2 ..
    query_params = set(sms.split())
    query_params = query_params.difference(blacklist_words)
    service = get_first_matching(service_list, query_params)
    service_type = get_first_matching(service_type_list, query_params)
    service_type = get_first_matching(service_type_list, query_params)
    if service == None or service_type == None:
        return ""
    query_params.remove(service)
    query_params.remove(service_type)
    query_params = list(query_params)

    # api_spec = requests.get(
    #     discovery_end_point,
    #     params={'serviceId': client_code, 'serviceName': call_name})
    api_spec = []
    resp = make_request(service, service_type, query_params, api_spec)
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
