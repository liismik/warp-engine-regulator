import requests
import time
import json

url = 'https://warp-regulator-bd7q33crqa-lz.a.run.app/api/'
myobj = {'name': 'Liisa',
         'email': 'liisamikola15@gmail.com'}

startTime = time.time()

start = requests.post(url + "start", data=myobj)
authorizationCode = start.json()['authorizationCode']
print(authorizationCode)
print(start.json()['message'])
print("Status: " + start.json()['status'])


def mainLoop():
    status = checkStatus()
    print(status.json())
    flowRate = ""
    intermix = 0.0
    try:
        flowRate = status.json()["flowRate"]
        intermix = status.json()["intermix"]
    except Exception as e:
        print("error")
    print("Intermix: " + str(intermix))
    print("Flowrate: " + str(flowRate))
    if str(flowRate) == "OPTIMAL":
        fuelOperations("OPTIMAL", intermix)
    if str(flowRate) == "HIGH":
        fuelOperations("HIGH", intermix)
    if str(flowRate) == "LOW":
        fuelOperations("LOW", intermix)

    time.sleep(1)
    stopTime = time.time()
    print("Time run: " + str(round(stopTime - startTime)) + "s")
    mainLoop()


def checkStatus():
    print("Checking status...")
    status = requests.get(url + "status?authorizationCode=" + str(authorizationCode))
    print(status.json())
    return status


def fuelOperations(flowRate, intermix):
    if flowRate == "HIGH":
        if intermix >= 0.5:
            # remove matter
            fuelChanges("matter", -0.2)
        elif intermix <= 0.5:
            fuelChanges("antimatter", -0.2)
        return
    if flowRate == "LOW" or flowRate == "OPTIMAL":
        if intermix >= 0.5:
            # add antimatter
            fuelChanges("antimatter", 0.2)
        elif intermix <= 0.5:
            # add matter
            fuelChanges("matter", 0.2)
        return


def fuelChanges(matterKind, amount):
    print("Adding " + str(round(amount, 2)) + " " + matterKind)
    fuelData = {'authorizationCode': authorizationCode,
                'value': amount}
    headers = {'content-type': 'application/json'}
    print(fuelData)
    requests.post(url + "adjust/" + matterKind, data=json.dumps(fuelData), headers=headers)


mainLoop()