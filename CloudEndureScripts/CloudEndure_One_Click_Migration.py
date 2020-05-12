#!/usr/bin/python

# =================================================================================================
#
#
# usage: CloudEndure_One_Click_Migration.py -u USERNAME -p PASSWORD -l LAUNCHTYPE -j PROJECT_NAME -c CONFIGFILE
#
#
# Arguments:
#
#   -u USERNAME, 	--username USERNAME
#                         user name for the CloudEndure account
#   -p PASSWORD, 	--password PASSWORD
#                         password for the CloudEndure account
#   -l LAUNCHTYPE, 	--launchtype LAUNCHTYPE
#                         launch type for the migration
# 	-j PROJECT_NAME, 	--project PROJECT_NAME
#                         CloudEndure's project name
#   -c CONFIGFILE	--configfile CONFIG_FILE
#						Config File name for blueprint settings 
#
#
# Required inputs: CloudEndure username and password, target server name
#
# Outputs: Will print to console the entire process:
#	1. CloudEndure Agent installation on the target server.
#	2. Blueprint settings.
#	3. Replication progress.
#	4. Target server launch progress.
#
#
# =================================================================================================
# Inbuilt modules
import requests
import os
import argparse
import json
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#User defined modules
import fetchToken
import getMachine_info
import install_agent
import replication
import launch_machine
import set_blueprint

###################################################################################################
def main():

# This is the main function, call the other functions to do the following:
# 	1. CloudEndure Agent installation on the target server.
#	2. Blueprint settings.
#	3. Replication progress.
#	4. Target server launch progress.
#
# Returns: 	nothing - will always exit

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user', required=True, help='User name')
	parser.add_argument('-p', '--password', required=True, help='Password')
	parser.add_argument('-l', '--launchtype', default='test')
   	parser.add_argument('-j', '--project', required=True, help='Project name')
   	parser.add_argument('-c', '--configfile', required=True)

	args = parser.parse_args()

	installation_token = fetchToken.get_token(args)
	print("installation_token", installation_token)
        if installation_token == -1:
            print("Failed to retrieve project installation token")
            return -1
#
	machine_id = getMachine_info.instanceData(args)
	print("returned Instance name ", " name : ", machine_id)
        args.agentname = machine_id.replace("\n","")
#	
	machine_id, project_id = install_agent.install_agent(args, installation_token)
#	#Check if we were able to fetch the machine id
	if machine_id == -1:
		print("Failed to retrieve machine id")
		return -1
	#
	# # Check replication status, set blueprint while waiting for it to complete
	replication.wait_for_replication(args, machine_id, project_id)
	#
	# # Setting the blueprint. Failing to do so won't fail the entire process
	if set_blueprint.set_blueprint(args, machine_id, project_id) == -1:
	 	print("Failed to set blueprint")
	#
	# # Launch the target instance on the cloud
	launch_machine.launch_target_machine(args, machine_id, project_id)

###################################################################################################

if __name__ == '__main__':
    main()
