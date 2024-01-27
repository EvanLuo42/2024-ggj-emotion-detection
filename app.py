from flask import Flask

app = Flask(__name__)


@app.get('/')
def is_smiling():
    file = open('is_smiling')
    text = file.read()
    file.close()
    return text
