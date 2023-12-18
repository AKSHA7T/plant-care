from http import client
from venv import logger
from flask import Flask, request, jsonify, render_template
import os

from flask_cors import CORS, cross_origin
from plant_care.utils.main_utils import decodeImage
from plant_care.pipeline.predict import PredictionPipeline
from plant_care.constants import *

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    return "Training done successfully!"



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    print("predict")
    if(request.json['plant_name'] == 'none') :
        return jsonify("Error: Plant Type Not Selected")
    image = request.json['image']
    name = request.json['plant_name']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predict(name)
    print(name, result)
    ans = f"Your {name}"
    if result == 'healthy':
        ans += " is healthy"
    else :
        ans += f" have {result}"
    return jsonify(ans)

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=8080) #local host

