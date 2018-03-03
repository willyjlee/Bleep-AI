import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.debug = True

client = MongoClient('mongodb://hacktech-2018:pdUKdnxVEIgjTivMejwpXXDICiXCWokDZx0uuTasc0W5CHiApUtCQ227TZXESrgYXzO7h4BuMGjQM14frshPsw==@hacktech-2018.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')

db = client['HackTech2018']

@app.route('/list_data', methods=['GET'])
def list_data():
    results = []
    for doc in db.VideoData.find():
        results.append({'id': doc['id'], 'transcript': doc['transcript']})
    return str(results)

@app.route('/retrieve_data', methods=['GET'])
def get_data_by_vid():
    video_id = request.args.get('video_id')
    if not video_id:
        return str({ 'error': 'Must specify the video_id parameter.'})

    results = db.VideoData.find_one({ "id": video_id })
    if results is not None:
        return str({'id': results['id'], 'transcript': results['transcript']})
    else:
        return str({ 'error': "No data found!" })

@app.route('/update_data', methods=['GET', 'PUT'])
def update_data_by_vid():
    video_id = request.args.get('video_id')
    transcript = request.args.get('transcript')
    if not video_id or not transcript:
        return str({ 'error': 'Must specify the video_id and transcript parameters.'})

    results = db.VideoData.find_one({ "id": video_id })
    if results is not None:
        db.VideoData.update_one({ "id": video_id }, {"$set": {"transcript": transcript}})
        finalResults = db.VideoData.find_one({ "id": video_id })
        return str({'id': finalResults['id'], 'transcript': finalResults['transcript']})
    else:
        return str({ 'error': "Id %s doesn't exists!" % video_id })

@app.route('/add_data', methods=['GET', 'POST'])
def add_data_by_vid():
    video_id = request.args.get('video_id')
    transcript = request.args.get('transcript')
    if not video_id or not transcript:
        return str({ 'error': 'Must specify the video_id and transcript parameters.'})

    results = db.VideoData.find_one({ "id": video_id })
    if results is not None:
        return str({ 'error': "Id %s already exists!" % video_id })
    else:
        insertResults = db.VideoData.insert_one({ "id": video_id, "transcript": transcript })
        interResults = db.VideoData.find_one({ "_id": insertResults.inserted_id })
        return str({'id': interResults['id'], 'transcript': interResults['transcript']})

@app.route('/delete_data', methods=['GET', 'DELETE'])
def delete_data_by_vid():
    video_id = request.args.get('video_id')
    if not video_id:
        return str({ 'error': 'Must specify the video_id parameter.'})

    results = db.VideoData.find_one({ "id": video_id })
    if results is not None:
        db.VideoData.delete_one({ "id": video_id })
        return str({ 'results': "Successfully deleted %s" % video_id })
    else:
        return str({ 'error': "Id %s was not found!" % video_id })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)

#LMtZU1AqHnk