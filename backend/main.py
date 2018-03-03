from flask import Flask
from resources.database import hello
app = Flask(__name__)

@app.route('/')
def hello_world():
  hello()
  return "Bitch this shit workin"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

