import cloudshell.api.cloudshell_api as api
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sch
import json
import sys



def get_cloudshell_session(credentialsFilePath = 'creds.json'):
    jsonfile = open(credentialsFilePath, 'r')
    credentials = json.load(jsonfile)
    jsonfile.close()
    #print credentials

    serverAddress = credentials.get('cloudshell login details').get('server address')
    domain = credentials.get('cloudshell login details').get('domain')
    username = credentials.get('cloudshell login details').get('user')
    password = credentials.get('cloudshell login details').get('password')
    session = api.CloudShellAPISession(host=serverAddress, username=username, password=password, domain=domain)
    print "successfully logged into Cloudshell"
    return session


def add_cloudshell_user(function_inputs_json=None):
    if function_inputs_json:
        inputs = json.loads(function_inputs_json)
        # parse the inputs from the list
        # inputs jason example: cs_input1 = inputs.get('admin script inputs').get(cs_input1)
        cs_username = inputs.get('admin script inputs').get('Username')
        cs_password = inputs.get('admin script inputs').get('Password')
        cs_email = inputs.get('admin script inputs').get('Email')
        cs_isAdmin_string = inputs.get('admin script inputs').get('Administrator')
        if cs_isAdmin_string.lower() == 'false':
            cs_isAdmin = False
        else:
            cs_isAdmin = True

        cs_groups = inputs.get('admin script inputs').get('Groups')
        if len(cs_groups) == 0:
            if cs_isAdmin == False:
                raise (Exception(
                    "your user is non admin, and there are no groups to add - please specify at least one group"))
            else:
                cs_isAdmin = True
                print "there is at least 1 group, adding user to the groups"





        else:
            cs_isAdmin = True

    pass

    cs_session = get_cloudshell_session()
    # use session to run your logic
    print "Adding a new user with the following details: "
    print "username is: {0}, password is:  {1}, Email is: {2}".format(cs_username,cs_password,cs_email)
    try:
        cs_session.AddNewUser(username=cs_username, password=cs_password, email=cs_email, isAdmin=cs_isAdmin, isActive=True)
        print "User created successfully"
    except:
        "some error"

    # verify the user was actually created - get the details of the new user

    user_check = cs_session.GetUserDetails(cs_username)
    if user_check.Email == cs_email:
        print ("New user verified according to Email address")
    else:
        print ("There is some error with user details, please check")

    if len(cs_groups) > 0:
        print "Adding user to the following groups: "
        for i in cs_groups:
            print i
            for attempt in range (2):
                try:
                    cs_session.AddUsersToGroup(usernames=[cs_username], groupName=i)
                except Exception as e:
                    if e.message.__contains__('Unable to find group named:'):
                        cs_session.AddNewGroup(groupName=i, description="added by admin script", groupRole='Regular')
                else:
                    break
            else:
                break

            print "breakpoint"




    return cs_username




debug_json_string = '''{ "admin script inputs": {
      "Username": "Shaul suck my balls",
      "Password": "qweqwe123",
      "Email": "shaul.b@quali.com",
      "Administrator": "True"
    }
} '''

# with groups
debug_json_string = '''{ "admin script inputs": {
      "Username": "dan suck my balls",
      "Password": "qweqwe123",
      "Email": "dan.m@quali.com",
      "Administrator": "True",
      "Groups": ""
      
           
    }
} '''

input_data = sys.stdin.read()
out = add_cloudshell_user(input_data)
print out





# qq = session.GetResourceDetails('DUT 3')
# session.SetResourceSharedState(
#     reservationId='3370d76a-f21b-42c6-8d75-459c374b9af4',
#     resourcesFullName=['DUT 3'],
#     isShared=True
# )
# pass
