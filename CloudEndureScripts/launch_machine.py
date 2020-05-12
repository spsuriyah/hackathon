import json
import requests
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import login_cred

HOST = login_cred.HOST

def launch_target_machine(args, machine_id, project_id):

# This function makes the HTTPS call out to the CloudEndure API and launches the target server on the Cloud
#
# Usage: launch_target_machine(args, machine_id, project_id)
# 	'args' is script user input
# 	'machine_id' is the CloudEndure replicatin machine ID
# 	'project_id' is the CloudEndure project ID
#
# Returns: 0 on success

	print("Launching target server")
	if args.launchtype == "test" or args.launchtype == "cutover":
		launchType = args.launchtype
		launchType = launchType.upper()
	session, resp, endpoint = login_cred.login(args)
	if session == -1:
		print("Failed to login")
		return -1
	items = {'machineId': machine_id}
	resp = session.post(url=HOST+endpoint+'projects/'+project_id+'/launchMachines', data=json.dumps({'items': [items], 'launchType': launchType }))
	if resp.status_code != 202:
		print('Error creating target machine!')
		print('Status code is: ', resp.status_code)
		return -1
	jobId = json.loads(resp.content)['id']


	isPending = True
	log_index = 0
	print("Waiting for job to finish...")
	while isPending:
		resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/jobs/'+jobId)
		job_status = json.loads(resp.content)['status']
		isPending = (job_status == 'STARTED')
		job_log = json.loads(resp.content)['log']
		while log_index < len(job_log):
			if 'cleanup' not in job_log[log_index]['message']:
				if 'security group' not in job_log[log_index]['message']:
					print(job_log[log_index]['message'])
			log_index += 1

		time.sleep(5)

	print('Target server creation completed!')
	return 0;
