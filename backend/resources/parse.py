import os


class Parser(object):
    def __init__(self):
        pass

    # returns an array of dictionaries with info for each word
    def parse(self, directory="samples", file_name="test.info"):
        caption_path = os.path.dirname(os.path.realpath(
            __file__)) + "/../" + directory + "/" + file_name
        print(caption_path)
        ret = []
        with open(caption_path) as f:
            content = f.readlines()
            for x in content:
                line_arr, obj = x.rstrip().split(), {}
                if len(line_arr) < 4: continue
                try:
                    obj["start"] = float(line_arr[0])
                except:
                    obj["start"] = -1.0
                try:
                    obj["end"] = float(line_arr[1])
                except:
                    obj["end"] = -1.0
                obj["word"] = line_arr[2]
                try:
                    obj["confidence"] = line_arr[3]
                except:
                    obj["confidence"] = -1.0
                ret.append(obj)
        return ret