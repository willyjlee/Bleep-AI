########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import os
import requests
import json

headers = {
    # Request headers
    #'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': '64edd068ee5140a7b6ce2c9790c4f7f2',
}

params = urllib.parse.urlencode({
    # Request parameters
    #'videoUrl': '{string}',
    #'language': 'English',
    #'externalId': '{string}',
    #'metadata': '{string}',
    # 'description': '{string}',
    # 'partition': '{string}',
    'callbackUrl': 'http://52.165.191.240:8080/callback?projectName=yo',
    # 'indexingPreset': '{string}',
    # 'streamingPreset': '{string}',
    # 'linguisticModelId': '{string}'
})

try:
    # body = open('/Users/lee/Documents/pprojects/HackTech2018/backend/video.mp4', 'rb')
    # conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
    # conn.request("POST", "/Breakdowns/Api/Partner/Breakdowns?name=dude&privacy=Public&%s" % params, body, headers)
    # response = conn.getresponse()
    # data = response.read()
    # print(data)
    # conn.close()

	url = "https://videobreakdown.azure-api.net/Breakdowns/Api/Partner/Breakdowns?name=video.mp4&privacy=Public&%s" % params
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print(dir_path)
	with open(os.path.join(dir_path, 'video.mp4'), 'rb') as f:
		files = {'video.mp4': f}
		bid = requests.post(url, files=files, headers=headers)
		print(bid.json())

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
