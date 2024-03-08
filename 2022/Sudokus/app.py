from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from forms import SudokuForm
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "AlwaysCreateAConfigKey"
csrf = CSRFProtect(app).init_app(app)

@app.route("/")
def index():
    form = SudokuForm()
    return(render_template("index.html", form=form))

@app.route("/", methods=["POST"])
def sudoku():
    cells = request.form.getlist("cell")
    cells = [cell if cell != '' else '0' for cell in cells] #Removing empty values and replacing for further validation
    print(np.reshape(cells, (9,9))) #Reshaping in sudoku size
    return cells    


if __name__ == "__main__":
    app.run(debug=True)
