import json
import login_cred

def get_token(args):

# This function fetch the project installation token
# Usage: get_token(args)
#       'args' is script user input (args.user, args.password, args.agentname)
#
# Returns:      -1 on failure
	HOST = 'https://console.cloudendure.com'
        endpoint = '/api/latest/'
        print("Fetching the installation token...")
        session, resp, endpoint = login_cred.login(args)
        if session == -1:
                print("Failed to login")
                return -1

        project_name = args.project

        projects_resp = session.get(url=HOST+endpoint+'projects')
        projects = json.loads(projects_resp.content)['items']
        # print "project in vm",projects

        project = [p for p in projects if project_name==p['name']]
        if not project:
                print('Error! No project with name ' + args.project+ ' found')
                return -1

        return project[0]['agentInstallationToken']
