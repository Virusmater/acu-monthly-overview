from flask import Flask, render_template, request

from src import parser

app = Flask(__name__)

@app.route("/")
def main():
    month = request.args.get('month')
    if not month:
        month = "November"
    events = parser.get_events(month)
    return render_template('main.html', events=events)
