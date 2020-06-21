from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.firestore import getNews, getNewsByCategory, getNewsByCategoryAndField, getNewsBySportAndLeague, incrementAction

API_KEY = "d63ddde6-30c0-4869-ab47-633b1d696dfb"

app = Flask(__name__)
CORS(app)

def toInt(tmpVal, default=0):
    if tmpVal is None or not tmpVal.isdigit:
        return default
    else:
        return int(tmpVal)

@app.route("/")
def news_all():
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0) * limit
    if api_key != API_KEY:
        return jsonify(message="Bad API key!")
    news = getNews(limit, offset)
    return jsonify(total=len(news), news=news)

@app.route("/<category>")
def news_category(category):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0) * limit
    if api_key != API_KEY:
        return jsonify(message="Bad API key!")
    news = getNewsByCategory(limit, offset, category)
    return jsonify(total=len(news), news=news)

@app.route("/<category>/<field>")
def news_cf(category, field):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0) * limit
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNewsByCategoryAndField(limit, offset, category, field)
    return jsonify(total=len(news), news=news)

@app.route("/Sport/<sport>/<league>")
def news_sl(sport, league):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0) * limit
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNewsBySportAndLeague(limit, offset, sport, league)
    return jsonify(total=len(news), news=news)

@app.route("/<action>/<_hash>", methods=['POST'])
def news_like(action, _hash):
    api_key = request.args.get("api_key")
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = incrementAction(_hash, action)
    return jsonify(total=len(news), news=news)

