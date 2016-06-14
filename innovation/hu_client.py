from db import Agent
import requests
from urllib import *

OK = 200
FAIL = 400

#Error Messages
err_resp= {
		1: "Sorry, I could not understand your command.Please try again.",# Input incorrect URL or Input non-valid value for ''mode'
		2: "Sorry,the command does not exist.Please try again", # Input the wrong querry. Valide querry are: Control , Status
		3: "Sorry, the service does not exist. Please try again.", #Input the wrong service. Valid services are: climatecontrol, battery
		4: "I could not communicate with the tv. Pleas, try again later", #car server is down
		5: "Sorry, please provide the channel name",
		6: "Sorry, please indicate you want to turn on or turn off the tv"
}

def get_service(hostname, service, query, timeout, **params):
		base_url = "http://{hostname}/api/{service}/{query}".format(
				hostname=hostname,
				service=service,
				query=query
		)
		url = base_url
		# Build the Request URL format
		if query == "change":
			if params['channel']:
				url = "{base_url}?{params}".format(
						base_url=base_url,
						params=urlencode(params)
				)
				response_str = "The TV has successfully changed to {0}.".format(params['channel'])
			else:
				return err_resp[5]
		elif query == 'record':
			if params['channel']:
				url = "{base_url}?{params}".format(
						base_url=base_url,
						params=urlencode(params)
				)
				response_str = "The TV channel {0} has started recording successfully.".format(params['channel'])
			else:
				return err_resp[5]
		elif query == 'stream':
			if params['channel']:
				url = "{base_url}?{params}".format(
						base_url=base_url,
						params=urlencode(params)
				)
				response_str = "The TV channel {0} has started streaming successfully.".format(params['channel'])
			else:
				return err_resp[5]
		elif query == 'turn':
			if params['state']:
				url = "{base_url}?{params}".format(
						base_url=base_url,
						params=urlencode(params)
				)
				response_str = "The TV channel has successfully turned {0}.".format(params['state'])
			else:
				return err_resp[6]
		else:
			return err_resp[3]

		# Make a http get srequest
		try:
			r = requests.get(url=url, timeout=timeout, verify=False)
			response = r.json()
			status = response.get("query_status")
			if status == "success": # In case of return Success Responses
				status = response.get("query_status")

			#############################################################################
			#############################################################################
			############################### hu connection ###############################
			#############################################################################
			#############################################################################

				# response_str = "The car has successfully tuned to {0}.".format(channel)
			else: #In case of return Error Responses
				response_str = error_code[4]
			return response_str
		# In case of Car server is down or not running
		except requests.ConnectionError or requests.Timeout as e:
			print e
			return err_resp[4]

def get_channel_name(freq):
	db = Agent('innovation')
	return db.get_channel_name_from_freq(freq)

if __name__ == '__main__':
	channel = get_channel_name('88.5FM')
	print get_service('10.3.22.100:8085', 'tv', 'change', 500, channel=channel)
