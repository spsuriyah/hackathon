import yaml
import json
import sys
import os
import login_cred

HOST = login_cred.HOST
INSTANCE_TYPE = "c4.large"

def set_blueprint(args, machine_id, project_id):

# This function makes the HTTPS call out to the CloudEndure API to set the serve blueprint before launching it on Cloud
# This function will set the instanceType, subnetID, and the securityGroupIDs.
#
# Usage: set_blueprint(args, machine_id, project_id)
# 	'args' is script user input (args.user, args.password, args.agentname)
# 	'machine_id' is the CloudEndure replicatin machine ID
# 	'project_id' is the CloudEndure project ID
#
# Returns: 	0 on success, -1 on failure

	print("Setting blueprint...")

	session, resp, endpoint = login_cred.login(args)
	if session == -1:
		print("Failed to login")
		return -1

	blueprints_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/blueprints')
	blueprints = json.loads(blueprints_resp.content)['items']

	blueprint = [bp for bp in blueprints if machine_id==bp['machineId']]
	if len(blueprint) == 0:
		return -1

	print("yaml ", args.configfile)
	with open(os.path.join(sys.path[0], args.configfile), 'r') as ymlfile:
	    config = yaml.load(ymlfile)
	print(config[args.agentname]['subnetIDs'])

	configSubnet = config[args.agentname]['subnetIDs']
        configSg = config[args.agentname]['securitygroupIDs']

	blueprint = blueprint[0]
	if config[args.agentname]['iamRole'].lower() != "none":
		blueprint['iamRole'] = config[args.agentname]['iamRole']
	blueprint['instanceType']= config[args.agentname]['instanceType']
	blueprint['subnetIDs']=configSubnet
	blueprint['securityGroupIDs']=configSg
	blueprint['machineId']=machine_id
	blueprint['publicIPAction'] = 'DONT_ALLOCATE'
	blueprint['privateIPAction'] = 'CREATE_NEW'
	

	resp = session.patch(url=HOST+endpoint+'projects/'+project_id+'/blueprints/'+blueprint['id'],data=json.dumps(blueprint))
	if resp.status_code != 200:
		print("ERROR: Updating blueprint failed for machine: " + args.agentname+", invalid blueprint config....")
		return -1

	print("Blueprint for machine: " + args.agentname+ " updated....")
	return 0
