from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(
        status = True,msg = "I am best at flask"
    )

@app.route("/get_weekday/<int:weekday>")
def get_weekday(weekday):
    return jsonify(status = [
        ["Sunday", "Sun"],
        ["Mondey", "Mon"],
        ["Tuesday", "Tue"]
    ][weekday-1])