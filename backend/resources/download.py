from pytube import YouTube
import os


class VideoDownloader(object):
    def __init__(self):
        pass

    def download(self, url="", path=None):
        try:
            YouTube(url).streams.filter(
                    subtype="mp4", progressive=True).order_by('resolution').asc().first().download(output_path=path, filename="video")
        except:
            raise ValueError("Something went wrong with video download")
