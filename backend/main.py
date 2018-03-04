from flask import Flask, request, jsonify
from flask_cors import CORS
from resources.download import VideoDownloader
from resources.parse import Parser
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json
import requests
from resources.media_services import processVideo

app = Flask(__name__)
CORS(app)
download_handler = VideoDownloader()
parser = Parser()

client = MongoClient('mongodb://hacktech-2018:pdUKdnxVEIgjTivMejwpXXDICiXCWokDZx0uuTasc0W5CHiApUtCQ227TZXESrgYXzO7h4BuMGjQM14frshPsw==@hacktech-2018.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')
db = client['HackTech2018'].VideoData

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '64edd068ee5140a7b6ce2c9790c4f7f2',
}


@app.route('/')
def hello_world():
    return "Welcome Bitch"


@app.route('/callback', methods=['POST'])
def callback():
	bid = request.args.get('id')
	state = request.args.get('state')
	print('bid: {} state: {}'.format(bid, state))
	url_break = "https://videobreakdown.azure-api.net/Breakdowns/Api/Partner/Breakdowns/%s" % bid
	breakds = requests.get(url_break, headers=headers)
	print(breakds.text)
	return "ok..."


@app.route('/download')
def download():
    video_id = request.args.get('video_id')
    print(video_id)
    download_handler.download('https://www.youtube.com/watch?v=' + video_id)
    return "installed that shit"


@app.route('/path')
def path():
    video_id = request.args.get('id')
    print(video_id)
    processVideo(os.path.join('videos', 'video.mp4'))
    return jsonify(parser.parse())


@app.route('/database')
def database():
    results = []
    for doc in db.find():
        results.append({'id': doc['id'], 'transcript': doc['transcript']})
    return str(results)

def get_root_path(internal_path=""):
    return os.path.join(app.root_path, internal_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))

