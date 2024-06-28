
from flask import Flask, request, render_template, jsonify
from src.queue.publish import create_queue_connection,publish_message
import uuid


app = Flask(__name__)


@app.route('/execute', methods=['POST'])
def main():
    if request.method == 'POST':
        request_json = request.get_json()
        request_json["id_"] = str(uuid.uuid4())
        try:
            publish_message(rabbit_connection,request_json)
        except Exception as e:
            return jsonify({"status":500,"id_":request_json["id_"]})
    return jsonify({"status":200,"id_":request_json["id_"]})


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    global rabbit_connection
    rabbit_connection = create_queue_connection()
    app.run(debug=False)