from flask import Flask, request
from resources.download import VideoDownloader
import os
import requests

app = Flask(__name__)
download_handler = VideoDownloader()

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '64edd068ee5140a7b6ce2c9790c4f7f2',
}

@app.route('/')
def hello_world():
  return "Welcome Bitch"

@app.route('/callback', methods= ['POST'])
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
  youtube_path = request.args.get('path')
  print(youtube_path)
  download_handler.download('https://www.youtube.com/' + youtube_path)
  return "Installed that shit"

def get_root_path(internal_path=""):
    return os.path.join(app.root_path, internal_path)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

