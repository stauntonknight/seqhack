import requests
from collections import OrderedDict
from urllib import urlencode
import schedule, time
import cjson
import smstohttp

user_name="nitkkr.vivek@gmail.com"
password="123456789"

def get_messages():
	params = OrderedDict([('email', user_name), ('password', password)])
	try:
		content = requests.get('http://smsgateway.me/api/v3/messages', params=urlencode(params)).content
		res = cjson.decode(content)
		if res["success"]:
			for each_res in res["result"]:
				if each_res["status"] == "received":
					print smstohttp.main(each_res["message"])
					

	except requests.exceptions.RequestException as e:
		print e

schedule.every(0.01).minutes.do(get_messages)

while True:
	schedule.run_pending()
	time.sleep(1)

