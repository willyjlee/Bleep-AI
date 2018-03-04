from flask import Flask, request, jsonify
from flask_cors import CORS
from resources.download import VideoDownloader
from resources.parse import Parser
from resources.database import DatabaseHandler
from resources.sentiment import sentiment_analysis
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json
import requests
from resources.media_services import processVideo

app = Flask(__name__)
CORS(app)
download_handler = VideoDownloader()

client = MongoClient('mongodb://hacktech-2018:pdUKdnxVEIgjTivMejwpXXDICiXCWokDZx0uuTasc0W5CHiApUtCQ227TZXESrgYXzO7h4BuMGjQM14frshPsw==@hacktech-2018.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')
db = DatabaseHandler(client['HackTech2018'].VideoData)

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

'''
@app.route('/download')
def download():
    video_id = request.args.get('video_id')
    print(video_id)
    download_handler.download('https://www.youtube.com/watch?v=' + video_id, 'videos')
    return "installed that shit"
'''

@app.route('/path')
def path():
    video_id = request.args.get('id')
    print(video_id)

    # metadata
    title = request.args.get('title')
    publisher = request.args.get('publisher')
    publisher_link = request.args.get('publisher_link')
    metadata = {
        "title": title,
        "publisher": publisher,
        "publisher_link": publisher_link
    }

    if db.exists(video_id):
        print('db has entry')
        results = db.fetch(video_id)
        return jsonify({
            "transcript": results["transcript"],
            "sentiment": results["sentiment"],
            "metadata": results["metadata"]
        })
    print('db does not have entry')
    download_handler.download('https://www.youtube.com/watch?v=' + video_id, 'videos')

    processVideo(os.path.join('videos', 'video.mp4'), os.path.join('resources', 'data', 'transcript.info'))
    parser = Parser()
    transcript = parser.parse(os.path.join('resources', 'data'), 'transcript.info')
    sentiment_data = sentiment_analysis(transcript)
    db.push(video_id, transcript, sentiment_data, metadata)
    return jsonify({ "transcript": transcript, "sentiment": sentiment_data, "metadata": metadata })


@app.route('/database')
def database():
    results = []
    for doc in db.find():
        results.append({'id': doc['id'], 'transcript': doc['transcript']})
    return str(results)

@app.route('/fetch_entries')
def fetch_entries():
    return jsonify(db.fetch_entries(num_entries=5))

def get_root_path(internal_path=""):
    return os.path.join(app.root_path, internal_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))

