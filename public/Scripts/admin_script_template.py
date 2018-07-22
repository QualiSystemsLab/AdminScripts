import cloudshell.api.cloudshell_api as api
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sch
import json
import sys



def get_cloudshell_session(credentialsFilePath = 'c:\cloudshell_admin_scripts\creds.json'):
    jsonfile = open(credentialsFilePath, 'r')
    credentials = json.load(jsonfile)
    jsonfile.close()
    #print credentials

    serverAddress = credentials.get('cloudshell login details').get('server address')
    domain = credentials.get('cloudshell login details').get('domain')
    username = credentials.get('cloudshell login details').get('user')
    password = credentials.get('cloudshell login details').get('password')
    session = api.CloudShellAPISession(host = serverAddress,username = username, password = password, domain= domain)
    return session

def main_function_name (function_inputs = None):
    if function_inputs:
        # parse inputs
        pass

    cs_session = get_cloudshell_session()
    # use session to run your logic
    users = cs_session.GetAllUsersDetails().Users[0].Name
    return users



a = main_function_name()
print a





# qq = session.GetResourceDetails('DUT 3')
# session.SetResourceSharedState(
#     reservationId='3370d76a-f21b-42c6-8d75-459c374b9af4',
#     resourcesFullName=['DUT 3'],
#     isShared=True
# )
# pass
