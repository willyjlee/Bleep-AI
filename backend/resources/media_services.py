import requests
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess
#import variables
from time import sleep
#from parse import Parser
import os

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

def uploadInputFile(assetId, uploadUrl, filepath):
    block_blob_service = BlockBlobService(account_name='wordsplitter', account_key=blob_account_key)
    block_blob_service.create_blob_from_path('asset-' + assetId[12:], 'blobby.mp4', filepath, content_settings=ContentSettings(content_type='video/mp4'))

def addMetadata(token, assetId):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/CreateFileInfos?assetid='%s'" % assetId
    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Authorization': "Bearer %s" % token,
    }

    requests.request("GET", url, headers=headers)

# returns Job ID
def startIndexingJob(token, assetId):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/Jobs"

    payload = "{\"Name\":\"Indexerv2Job\",\"InputMediaAssets\":[{\"__metadata\":{\"uri\": \"https://wordsplitter.restv2.centralus.media.azure.net/api//Assets('%s')\"}}],\"Tasks\":[{\"Configuration\":\"{'Version':'1.0','Features':[{'Options':{'Formats':['WebVtt','TTML'],'Language':'EnUs','Type':'RecoOptions'},'Type':'SpReco'}]}\",\"MediaProcessorId\":\"nb:mpid:UUID:1927f26d-0aa5-4ca1-95a3-1a3f95b0f706\",\"TaskBody\": \"<?xml version=\\\"1.0\\\" encoding=\\\"utf-8\\\"?><taskBody><inputAsset>JobInputAsset(0)</inputAsset><outputAsset assetName=\\\"foobar.mp4\\\">JobOutputAsset(0)</outputAsset></taskBody>\"}]}" % assetId

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
    js = response.json()
    return js["d"]["Id"], js["d"]["OutputMediaAssets"]["__deferred"]["uri"]


def getJobState(token, jobId):
    url = "https://wordsplitter.restv2.centralus.media.azure.net/api/Jobs('%s')" % jobId

    querystring = {"$select":"State"}

    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Cache-Control': "no-cache",
        'Postman-Token': "11e6586d-148e-755e-42ae-875850d48382",
        'Authorization': "Bearer %s" % token
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.text:
        return -1
    return response.json()["State"]

def getOutput(outputUrl, token):
    headers = {
        'x-ms-version': "2.15",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'DataServiceVersion': "3.0",
        'MaxDataServiceVersion': "3.0",
        'User-Agent': "azure media services postman collection",
        'Authorization': "Bearer %s" % token,
        'Cache-Control': "no-cache",
        'Postman-Token': "867114be-9e9a-5c0b-2209-5e405093abcf"
    }
    response = requests.request("GET", outputUrl, headers=headers)
    return response.json()["value"][0]["Id"]

def download(container):
    block_blob_service = BlockBlobService(account_name='wordsplitter', account_key=blob_account_key)
    gen = block_blob_service.list_blobs(container)
    blob_name = None
    for blob in gen:
        if blob.name.endswith('.info'):
            blob_name = blob.name
    block_blob_service.get_blob_to_path(container, blob_name, os.path.join('data', 'transcript.info'))
    print('...downloaded transcript.info')

def processVideo(videoPath):
    token = getADToken()
    assetId = createAsset(token, "iamconfused")
    uploadUrl = createSASLocator(token, assetId)
    uploadInputFile(assetId, uploadUrl, videoPath)
    addMetadata(token, assetId)
    jobId, outputUrl = startIndexingJob(token, assetId)

    state = getJobState(token, jobId)
    while state != 3:
        print('waiting state: %d' % state)
        sleep(1)
        state = getJobState(token, jobId)

    outputAssetId = getOutput(outputUrl, token)
    download('asset-' + outputAssetId[12:])

