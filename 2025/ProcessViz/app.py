from flask import Flask
from process_manager import *

app = Flask(__name__)

@app.route("/processes")
def display_processes():
    return get_processes()

if __name__ == "__main__":
    app.run(debug=True)