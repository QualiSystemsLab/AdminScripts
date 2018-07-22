import cloudshell.api.cloudshell_api as api
import cloudshell.api.common_cloudshell_api
import json
import sys

def get_cloudshell_session(credentialsFilePath = 'creds.json'):
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
    if function_inputs is None:
        return "Missing JSON data"

    parameters = json.loads(function_inputs)

    if "NewAttributeName" not in parameters.keys():
        return "Missing new attribute name"

    session = get_cloudshell_session('creds.json')
    # use session to run your logic

    param_resourceFamily = ''
    param_resourceModel = ''
    param_attributeValues = []
    param_showAllDomains  = True
    param_resourceFullName   = ''
    param_includeSubResources  = True
    param_resourceAddress  = ''
    param_resourceUniqueIdentifier  = ''
    param_includeExcludedResources = True

    if "ResourceFamily" in parameters.keys():
        param_resourceFamily = parameters.get("ResourceFamily")

    if "ResourceModel" in parameters.keys():
        param_resourceModel = parameters.get("ResourceModel")

    if "AttributeValues" in parameters.keys():
        if (parameters.get("AttributeValues") != ''):
            param_attributeValues = parameters.get("AttributeValues")

    if "ShowAllDomains" in parameters.keys():
        if (parameters.get("ShowAllDomains") == "True"):
            param_showAllDomains = True
        else:
            param_showAllDomains = False

    if "ResourceFullName" in parameters.keys():
        param_resourceFullName = parameters.get("ResourceFullName")

    if "IncludeSubResources" in parameters.keys():
        if (parameters.get("IncludeSubResources") == "True"):
            param_includeSubResources = True
        else:
            param_includeSubResources = False

    if "ResourceAddress" in parameters.keys():
        param_resourceAddress = parameters.get("ResourceAddress")

    if "ResourceUniqueIdentifier" in parameters.keys():
        param_resourceUniqueIdentifier = parameters.get("ResourceUniqueIdentifier")

    if "IncludeExcludedResources" in parameters.keys():
        if (parameters.get("IncludeExcludedResources") == "True"):
            param_includeExcludedResources =  True
        else:
            param_includeExcludedResources = False

            #Get attribute from JSON
    param_attributeName = parameters.get("NewAttributeName")
    param_attributeValue = ""

    if "NewAttributeValue" in parameters.keys():
        param_attributeValue = parameters.get("NewAttributeValue")

    resources = []

    try:
        resources = session.FindResources(
            resourceFamily = param_resourceFamily,
            resourceModel = param_resourceModel,
            attributeValues = param_attributeValues,
            showAllDomains = param_showAllDomains,
            resourceFullName = param_resourceFullName,
            includeSubResources = param_includeSubResources,
            resourceAddress = param_resourceAddress,
            resourceUniqueIdentifier = param_resourceUniqueIdentifier,
            includeExcludedResources = param_includeExcludedResources).Resources

    except cloudshell.api.common_cloudshell_api.CloudShellAPIError as e:
        print e.message

    affectedResources = []

    for currResource in resources:
        try:
            session.SetAttributeValue(currResource.FullPath, param_attributeName, param_attributeValue)
            affectedResources.append(currResource.FullName)

            print "Changed ", param_attributeName, " in Resource ", currResource.FullName

        except cloudshell.api.common_cloudshell_api.CloudShellAPIError as e:
            print "resource: ", currResource.FullName, " Path: ", currResource.FullPath, \
                " - have failed to change attribute: ", param_attributeName, " to Value: ", param_attributeValue, \
                " Reason: ", e.message

    return affectedResources

# input_data = '{' \
#              '"ResourceFamily":"DUT", ' \
#              '"ResourceModel":"DUT Model",' \
#              '"NewAttributeName":"User", ' \
#              '"NewAttributeValue":"Natti",'\
#              '"IncludeExcludedResources":true' \
#              '}'

#input_data = '{"Description":"Change bulk resources attributes by...","ResourceFamily":"","ResourceModel":"DUT Model","AttributeValues":"","ShowAllDomains":"True","ResourceFullName":"","IncludeSubResources":"True","ResourceAddress":"","ResourceUniqueIdentifier":"","IncludeExcludedResources":"True","NewAttributeName":"User","NewAttributeValue":"LoserServer","file_name":"ChangeBulkResources.py"}'

input_data = sys.stdin.read()
output = main_function_name(input_data)
print "hello there!"
print output