import os
import requests
import json
import login_cred

WIN_FOLDER = "c:\\temp"
LINUX_FOLDER = "/tmp"

def install_agent(args, installation_token):

# This function makes the HTTPS call out to the CloudEndure API and waits for the replication to complete
#
# Usage: wait_for_replicaiton(args, machine_id, project_id)
# 	'args' is script user input (args.user, args.password, args.agentname, args.project)
#
#
# Returns: 	0 on success, -1 on failure

	# Check if it's a windows or not
	HOST = login_cred.HOST
	if os.name == 'nt':
		# Make sure the temp folder exitts, the installer will run from it
		if not os.path.exists(WIN_FOLDER):
			os.mkdir(WIN_FOLDER)
		os.chdir(WIN_FOLDER)
		fname = 'installer_win.exe'
		cmd = 'echo | ' +fname + ' -t ' + installation_token + ' --no-prompt'
	else:
		os.chdir(LINUX_FOLDER)
		fname = 'installer_linux.py'
		cmd = 'sudo python ' +fname + ' -t ' + installation_token + ' --no-prompt'

	url = HOST + '/' + fname
	request = requests.get(url)
	open(fname , 'wb').write(request.content)

	ret = os.system(cmd)
	# Return value of agent installer should be 0 if succeded
	if ret != 0:
		print("Failed installing CloudEndure agent")
		return -1, -1

	session, resp, endpoint= login_cred.login(args)

	if session == -1:
		print("Failed to login")
		return -1, -1

	# Fetch the CloudEndure project ID in order to locate the machine itself
	projects_resp = session.get(url=HOST+endpoint+'projects')
	projects = json.loads(projects_resp.content)['items']

	project_id = None
	machine_id = None

	# Fetch the CloudEndure machine ID in order monitor the replication progress and launch the target server
	print('Getting machine id...')
	for project in projects:
		project_id = project['id']

		machines_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines')
		machines = json.loads(machines_resp.content)['items']

		machine_id = [m['id'] for m in machines if args.agentname.lower() == m['sourceProperties']['name'].lower()]

		
		if machine_id:
			break

	if not machine_id:
		print('Error! No agent with name ' + args.agentname + ' found')
		return -1, -1

	return machine_id[0].encode('ascii','ignore'), project_id
