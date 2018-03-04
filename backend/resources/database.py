class DatabaseHandler(object):
    def __init__(self, db):
        self.database = db

    def push(self, video_id, transcript):
        self.database.insert_one({ "id": video_id, "transcript": transcript })

    def exists(self, video_id):
        return self.database.find_one({ "id": video_id }) is not None

    def fetch(self, video_id):
        return self.database.find_one({ "id": video_id })