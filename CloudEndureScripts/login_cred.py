import requests
import json

HOST = 'https://console.cloudendure.com'

def login(args):

# This function makes the HTTPS call out to the CloudEndure API to login using the credentilas provided
#
# Usage: login(args)
# 	'args' is script user input (args.user, args.password, args.agentname)
#
# Returns: 	-1 on failure
#			session, response, endpoint on success

	endpoint = '/api/latest/'
	session = requests.Session()
	session.headers.update({'Content-type': 'application/json', 'Accept': 'text/plain'})
	resp = session.post(url=HOST+endpoint+'login', data=json.dumps({'username': args.user, 'password': args.password}))
	if resp.status_code != 200 and resp.status_code != 307:
		print "Bad login credentials"
		return -1, -1, -1
	#print 'Logged in successfully'


	# Check if need to use a different API entry point and redirect
	if resp.history:
		endpoint = '/' + '/'.join(resp.url.split('/')[3:-1]) + '/'
		resp = session.post(url=HOST+endpoint+'login', data=json.dumps({'username': args.user, 'password': args.password}))

	try:
		session.headers.update({'X-XSRF-TOKEN' : resp.cookies['XSRF-TOKEN']})
	except:
		pass

	return session, resp, endpoint

###################################################################################################
