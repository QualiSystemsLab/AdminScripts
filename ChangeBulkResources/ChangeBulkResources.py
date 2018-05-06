import cloudshell.api.cloudshell_api as api
import cloudshell.api.common_cloudshell_api
import json
import sys

username = 'admin'
password = 'admin'
server = 'localhost'
domain = 'Global'
new_server = 'localhost'





def get_cloudshell_session(credentialsFilePath = 'c:\cloudshell_admin_scripts\creds.json'):
    jsonfile = open(credentialsFilePath, 'r')
    credentials = json.load(jsonfile)
    jsonfile.close()

    serverAddress = credentials.get('cloudshell login details').get('server address')
    domain = credentials.get('cloudshell login details').get('domain')
    username = credentials.get('cloudshell login details').get('user')
    password = credentials.get('cloudshell login details').get('password')
    session = api.CloudShellAPISession(host = serverAddress,username = username, password = password, domain= domain)
    return session

def main_function_name (function_inputs = None):
    if function_inputs is None
        return "Missing JSON data"

    parameters = json.loads(function_inputs)

    session = get_cloudshell_session()
    # use session to run your logic


    param_resourceFamily = ''
    param_resourceModel = ''
    param_attributeValues = []
    param_showAllDomains  = False
    param_resourceFullName   = ''
    param_includeSubResources  = True
    param_resourceAddress  = ''
    param_resourceUniqueIdentifier  = ''
    param_includeExcludedResources = True

    #resourceFamily (str)
    #resourceModel (str)
    #attributeValues (list[AttributeNameValue])
    #showAllDomains (bool)
    #resourceFullName  (str)
    #includeSubResources (bool)
    #resourceAddress (str)
    #resourceUniqueIdentifier (str)
    #includeExcludedResources (bool)

    #Get attribute from JSON
    param_attributeName = ""
    param_attributeValue = ""

    resources = session.FindResources(
        resourceFamily = param_resourceFamily,
        resourceModel = param_resourceModel,
        attributeValues = param_attributeValues,
        showAllDomains = param_showAllDomains,
        resourceFullName = param_resourceFullName,
        resourceAddress = param_resourceAddress,
        resourceUniqueIdentifier = param_resourceUniqueIdentifier,
        includeExcludedResources = param_includeExcludedResources).Resources

    for currResource in resources:
        try:
            session.SetAttributeValue(currResource.FullPath, param_attributeName, param_attributeValue)
        except cloudshell.api.common_cloudshell_api.CloudShellAPIError as e:
            print "resource: ", currResource.FullName, " Path: ", currResource.FullPath, \
                " - have failed to change attribute: ", param_attributeName


    return resources

input_data = ""

output = main_function_name(input_data)
print output

