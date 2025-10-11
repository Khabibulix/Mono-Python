from flask import Flask, render_template, request, jsonify
from process_manager import *

app = Flask(__name__)

@app.route("/")
def display_processes():
    return render_template('index.html', get_processes=get_processes())


@app.route("/process/<int:pid>", methods=["GET"])
def process(pid):
    return get_infos_for_process_with_pid(pid)

if __name__ == "__main__":
    app.run(debug=True)