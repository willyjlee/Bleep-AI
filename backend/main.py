from flask import Flask, request
from resources.database import hello
from resources.download import VideoDownloader
import os

app = Flask(__name__)
download_handler = VideoDownloader()

@app.route('/')
def hello_world():
  return "Welcome Bitch"

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

