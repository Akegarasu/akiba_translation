from flask import Flask, request, jsonify
from manager import *

app = Flask(__name__)


@app.route('/api/auto', methods=['POST'])
def add_auto():
    if request.json:
        task = request.json
        result = execute.delay(task)
        return jsonify({'task_id': result.id})


@app.route('/api/get_task=<string:task_id>', methods=['GET'])
def get_task_result(task_id):
    result = {
        'task_id': task_id,
        'state': celery.AsyncResult(task_id).state,
        'result': celery.AsyncResult(task_id).result
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=9090)
