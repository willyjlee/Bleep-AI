from pytube import YouTube
import os


class VideoDownloader(object):
    def __init__(self):
        pass

    def download(self, url=""):
        try:
            YouTube(url).streams.filter(
                    subtype="mp4", progressive=True).order_by('resolution').asc().first().download()
        except:
            raise ValueError("Something went wrong with video download")
