import requests

# returns token
def getADToken():
    url = "https://login.microsoftonline.com/octabytes.onmicrosoft.com/oauth2/token"

    payload = "grant_type=client_credentials&client_id=763758c9-bc20-48de-9b96-65048d646719&client_secret=RqpaGOO7jPGxFCG8oOw%2F3yVWETPm1MgrqIq0uPXSJRg%3D&resource=https%3A%2F%2Frest.media.azure.net"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Keep-Alive': "true",
        'Cache-Control': "no-cache",
        'Postman-Token': "9c4bade5-d92c-15d7-5038-ed459ca0d8f9"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()['access_token']

# returns asset id
def createAsset(token, name):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/Assets"

    payload = "{\"Name\":\"%s\"\n}" % name
    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Authorization': "Bearer %s" % token,
        'Cache-Control': "no-cache",
        'Postman-Token': "54cf30c0-b454-a860-b8af-1c33a1ab1b53"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()['Id']

# returns upload url
def createSASLocator(token, assetId):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/Locators"

    payload = "{\"AccessPolicyId\":\"nb:pid:UUID:f48be184-bf7b-47f5-a542-e9c96dde3db2\",\"AssetId\":\"%s\",\"Type\":1\n}" % assetId
    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Authorization': "Bearer %s" % token,
        'Cache-Control': "no-cache",
        'Postman-Token': "2a6a5229-a2c3-ab36-1610-d508a907db33"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()["Path"]

def uploadInputFile(uploadUrl, fileName, filePath):
    headers = {
        'x-ms-blob-type': "BlockBlob",
        'Cache-Control': "no-cache",
        'Postman-Token': "780f0000-7a4f-4eba-b4b6-870117e92cdf"
    }

    with open(filePath, 'rb') as f:
        files = {}
        files[fileName] = f
        requests.request("PUT", uploadUrl, files=files, headers=headers)

def addMetadata(assetId):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/CreateFileInfos"

    querystring = {"assetid":"'%s'" % assetId}

    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Cache-Control': "no-cache",
        'Postman-Token': "131da290-d6eb-c61c-5614-715ac30d2bb3"
    }

    requests.request("GET", url, headers=headers, params=querystring)

def processVideo(videoPath):
    token = getADToken()
    assetId = createAsset(token, "lolwatchmenow")
    print(assetId)
    uploadUrl = createSASLocator(token, assetId)
    uploadInputFile(uploadUrl, 'BigBuckBunny.mp4', videoPath)
    addMetadata(assetId)

