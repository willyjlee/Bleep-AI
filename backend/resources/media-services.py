import requests
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess
from variables import blob_account_key

blob_name = 'blobby.mp4'

# returns token
def getADToken():
    url = "https://login.microsoftonline.com/octabytes.onmicrosoft.com/oauth2/token"

    payload = "grant_type=client_credentials&client_id=763758c9-bc20-48de-9b96-65048d646719&client_secret=RqpaGOO7jPGxFCG8oOw%2F3yVWETPm1MgrqIq0uPXSJRg%3D&resource=https%3A%2F%2Frest.media.azure.net"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Keep-Alive': "true"
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
        'Authorization': "Bearer %s" % token
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
        'Authorization': "Bearer %s" % token
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()["Path"]

def uploadInputFile(uploadUrl, filepath):
    block_blob_service = BlockBlobService(account_name='wordsplitter', account_key=blob_account_key)
    block_blob_service.create_blob_from_path('asset-d63d7b5a-9d33-4ff2-b8b7-9153ec48e0fd', blob_name, filepath, content_settings=ContentSettings(content_type='video/mp4'))

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

# returns Job ID
def startIndexingJob(token, assetId):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/Jobs"

    payload = "{\"Name\":\"Indexer v2 HackTech Job\",\"InputMediaAssets\":[{\"__metadata\":{\"uri\": \"https://wordsplitter.restv2.centralus.media.azure.net/api//Assets('%s')\"}}],\"Tasks\":[{\"Configuration\":\"{'Version':'1.0','Features':[{'Options':{'Formats':['WebVtt','TTML'],'Language':'EnUs','Type':'RecoOptions'},'Type':'SpReco'}]}\",\"MediaProcessorId\":\"nb:mpid:UUID:1927f26d-0aa5-4ca1-95a3-1a3f95b0f706\",\"TaskBody\": \"<?xml version=\\\"1.0\\\" encoding=\\\"utf-8\\\"?><taskBody><inputAsset>JobInputAsset(0)</inputAsset><outputAsset assetName=\\\"foobar.mp4\\\">JobOutputAsset(0)</outputAsset></taskBody>\"}]}" % assetId

    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json;odata=verbose",
        'Content-Type': "application/json;odata=verbose",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Authorization': "Bearer %s" % token
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()["d"]["Id"]



def processVideo(videoPath):
    token = getADToken()
    assetId = createAsset(token, "lolwatchmenow")
    print(assetId)
    uploadUrl = createSASLocator(token, assetId)
    uploadInputFile(uploadUrl, videoPath)
    addMetadata(assetId)
    jobId = startIndexingJob(token, assetId)
    print(jobId)

