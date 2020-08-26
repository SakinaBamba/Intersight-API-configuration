import intersight_rest as isREST
import json
import time
import requests
import os


##############
#              Authentication
##############

API_key = '*** Enter your API key here ***'
isREST.set_private_key(open("./SecretKey.txt", "r") .read())   #Path to your saved Secret key file
isREST.set_public_key(API_key)

##############
#              Initial values
##############

SerialNumber = input('Enter the Device Serial Number : ')
SecurityToken = input('Enter your Claim Code : ')

##############
#              Url paths
##############

Physical_Summary_path = '/compute/PhysicalSummaries'
Device_Claim_path = '/asset/DeviceClaims'
Server_Path = '/server/Profiles'



##############
#              Claim a device from Serial number and Claim code
##############

Device_Claim_body = {
    "SecurityToken": SecurityToken,
    "SerialNumber": SerialNumber
}

Claim_request = {
    "http_method": "post",
    "resource_path": Device_Claim_path,
    "body": Device_Claim_body
}

result1 = isREST.intersight_call(**Claim_request)

if result1.ok:
    print('Device Claimed successfully !!!')

if not result1.ok:
    print('Error: Could not claim device !')
    print(json.dumps(result1.json(), indent=4))
    print(result1.status_code)

##############
#              In this next section, a function is created to save every
#              new device claim asset moid number to a json file with its
#              respective serial number
##############

def append_asset_moid(asset_moid):

    with open('./DeviceClaimMoid.json','a') as f:

        json.dump(asset_moid, f)
        f.write(os.linesep)

my_dict = {SerialNumber:(result1.json())["Moid"]}
append_asset_moid(my_dict)


##############
#              Obtain the server profile Moid from the server profile list
##############

List_Server_Profiles_request = {
    "http_method": "get",
    "resource_path": Server_Path
}

result0 = isREST.intersight_call(**List_Server_Profiles_request)
if result0.ok:
    print('Looking through the Server Profiles List...')

if not result0.ok:
    print('Error: Could not obtain Server Profiles List')
    print(json.dumps(result0.json(), indent=4))
    print(result0.status_code)

x = (result0.json())["Results"]

print('Here is a list of all the server profiles : ')
for i in range(len(x)):
    print(x[i]["Name"])

ProfileName = input('Enter the Server Profile Name : ')

for i in range(len(x)):
    if x[i]["Name"] == ProfileName :
        Moid_sp = x[i]["Moid"]



print('Updating Physical Summary list ... Please allow 100 seconds')
time.sleep(100)


##############
#              Obtain Device Moid from Physical Summary
##############

PhysicalSummary_request = {
    "http_method": "get",
    "resource_path": Physical_Summary_path
}

result2 = isREST.intersight_call(**PhysicalSummary_request)
if result2.ok:
    print('Looking through the Physical Summary List...')


if not result2.ok:
    print('Error: Could not obtain Physical Summary')
    print(json.dumps(result2.json(), indent=4))
    print(result2.status_code)

y = (result2.json())["Results"]


for i in range(len(y)):
    if y[i]["Serial"] == SerialNumber :
        Moid_device = y[i]["Moid"]



##############
#              Server Profile association
##############

Server_Profile_path = '/server/Profiles/'+Moid_sp


Server_Profile_Asso_body = {"AssignedServer": {
                            "ClassId": "mo.MoRef",
                            "ObjectType": "compute.RackUnit",
                            "Moid" : Moid_device }}

profile_asso_request = {
    "http_method": "post",
    "resource_path": Server_Profile_path,
    "body": Server_Profile_Asso_body
}

result3 = isREST.intersight_call(**profile_asso_request)
if result3.ok:
    print('Server Profile associated to device successfully !!! : ')

if not result3.ok:
    print('Error: Could not associate Server Profile to device')
    print(json.dumps(result3.json(), indent=4))
    print(result3.status_code)




##############
#              Server Profile Deployment request
##############

Server_Deploy_body = {
    "Action": "Deploy"
}

Deploy_request = {
    "http_method": "post",
    "resource_path": Server_Profile_path,
    "body": Server_Deploy_body
}

result4 = isREST.intersight_call(**Deploy_request)
if result4.ok:
    print('Server Profile Deployed Successfully !!!')

if not result4.ok:
    print('Error: Could not deploy server profile ')
    print(json.dumps(result4.json(), indent=4))
    print(result4.status_code)


################# UNCOMMENT UNDER THIS TO UNCLAIM DEVICE ##################
# delete_serial = input('Enter the serial number of the device you would like to unclaim : ')
#
#
# with open('./DeviceClaimMoid.json','r') as f:
#     device_claim_data = json.load(f)
#     device_claim_moid = device_claim_data[delete_serial]
#
# Device_Unclaim_path = "/asset/DeviceClaims"
#
# Delete_request = {
#     "http_method": "delete",
#     "resource_path": Device_Unclaim_path,
#     "moid": device_claim_moid
# }
#
# result5 = isREST.intersight_call(**Delete_request)
#
# if result5.ok:
#     print('Device unclaimed successfully !!!')
#
# if not result5.ok:
#     print('Error: Could not unclaim device ')
#     print(json.dumps(result5.json(), indent=4))
#     print(result5.status_code)
