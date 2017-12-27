from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name,100)

    # TODO
    totaltweets = len(tweets)
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    positive, negative, neutral = 0.0, 0.0, 0.0
    for tweet in tweets:
        if analyzer.analyze(tweet)>0:
            positive = positive + 1
        elif analyzer.analyze(tweet)<0:
            negative = negative + 1
        else:
            neutral = neutral + 1
    positive = positive/totaltweets*100
    negative = negative/totaltweets*100
    neutral = neutral/totaltweets*100

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
