import _json
import cloudshell.api.cloudshell_api as api


username = 'admin'
password = 'admin'
server = 'localhost'
domain = 'Global'
new_server = 'localhost'

def GetSession ():
    session = api.CloudShellAPISession(
    username=username,
    password=password,
    domain=domain,
    host=server
    )
    return session

session = GetSession()
resources = session.FindResources(resourceFamily="Switch").Resources

for currResource in resources:
    print "resource name", currResource.FullName