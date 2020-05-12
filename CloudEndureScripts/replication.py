import json
import time
import login_cred

HOST = login_cred.HOST

def wait_for_replication(args, machine_id, project_id):

# This function makes the HTTPS call out to the CloudEndure API multiple times until replication to complete.
# Once it's done, the function will call set_blueprint in order to apply the blueprint settings before
# launching the target server.
#
# Usage: wait_for_replicaiton(args, machine_id, project_id)
# 	'args' is script user input (args.user, args.password, args.agentname)
# 	'machine_id' is the CloudEndure replicatin machine ID
# 	'project_id' is the CloudEndure project ID
#
# Returns: 	0 on success, -1 on failure

	# Looping until replication completes
	print("Waiting for Replication to complete")

	while True:
		session, resp, endpoint = login_cred.login(args)
		if session == -1:
			print "Failed to login"
			return -1

		# Waiting for replication to start and the connection to establish
		while True:
			try:
				machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)
				replication_status = json.loads(machine_resp.content)['replicationStatus']
				break
			except:
				print("Replication has not started. Waiting...")
				time.sleep(10)

		# Waiting for replication to start and the coneection to establish
		while replication_status != 'STARTED':
			print("Replication has not started. Waiting...")
			time.sleep(120)
			machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)
			replication_status = json.loads(machine_resp.content)['replicationStatus']

		while True:
			try:
				replicated_storage_bytes = json.loads(machine_resp.content)['replicationInfo']['replicatedStorageBytes']
				total_storage_bytes = json.loads(machine_resp.content)['replicationInfo']['totalStorageBytes']
				break
			except:
				print("Replication has not started. Waiting...")
				time.sleep(120)
				machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)

		# Replication has started, looping until complete, printing progress
		while True:
			try:
				last_consistency = json.loads(machine_resp.content)['replicationInfo']['lastConsistencyDateTime']
				backlog = json.loads(machine_resp.content)['replicationInfo']['backloggedStorageBytes']
				if backlog == 0:
					print("Replication completed. Target machine is launchable!")
					return 0
				else:
					print('Replication is lagging. Backlog size is '+ str(backlog))
					time.sleep(60)
			except:
				if replicated_storage_bytes == total_storage_bytes:
					print("Finalizing initial sync. Waiting...")
					time.sleep(60)
				else:
					print('Replicated '+ str(replicated_storage_bytes)+' out of '+str(total_storage_bytes)+' bytes')
					print("Will check again in 5 minutes. Waiting...")
					time.sleep(300)
			machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)
