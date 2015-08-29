import requests
from collections import OrderedDict
from urllib import urlencode
import schedule, time
import cjson
import smstohttp
import traceback

user_name="nitkkr.vivek@gmail.com"
password="123456789"
device_id = "12382"

def send_message(message, number):
    print "Trying to send SMS now to"
    print number
    print message
    params = OrderedDict([
        ('email', user_name),
        ('password', password),
        ('number', number),
        ('message', message),
        ('device', device_id)
        ])
    response = requests.get('http://smsgateway.me/api/v3/messages/send',
            params=urlencode(params)).content
    print response


def get_messages():
    params = OrderedDict([('email', user_name), ('password', password)])
    print "Getting messages"
    try:
        content = requests.get('http://smsgateway.me/api/v3/messages', params=urlencode(params)).content
        print "got messages"
        res = cjson.decode(content)
        if res["success"]:
            for each_res in res["result"]:
                print "message recd"
                if each_res["status"] == "received":
                    try:
                        print time.time() - 19800
                        print each_res["received_at"]
                        if time.time() - each_res["received_at"] - 43200> 60:
                            continue
                        print each_res
                        print "Qyering server"
                        message = smstohttp.main(each_res["message"])
                        print "Response :"
                        print message
                        if len(message) > 0:
                            print "Non zero len"
                            send_message(message, each_res["contact"]["number"])
                        else:
                            print "zero len"
                            send_message("Sorry, we could not find any results :(", each_res["contact"]["number"])
                    except Exception as e:
                        print "Error in handling"
                        send_message("Something went wrong. We did not handle all exceptions, sorry :(", each_res["contact"]["number"])
                        print e
                        traceback.print_exc()

    except requests.exceptions.RequestException as e:
        print e

schedule.every(1).minutes.do(get_messages)

while True:
    schedule.run_pending()
    time.sleep(1)
