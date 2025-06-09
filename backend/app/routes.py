from flask import Blueprint, jsonify, request
from .models import Match, Player
from .db import db
from .scraper import scrape_matches, scrape_stats

main_routes = Blueprint("main_routes", __name__)

@main_routes.route('/scrape-and-save', methods=['GET'])
def scrape_and_save():
    data = scrape_matches()
    for m in data:
        match = Match(title=m["title"], date=m["date"], location=m["location"], result=m["result"])
        db.session.add(match)
    db.session.commit()
    return jsonify({"status": "Saved", "matches": len(data)})

@main_routes.route('/matches', methods=['GET'])
def get_matches():
    matches = Match.query.all()
    return jsonify([{
        "title": m.title,
        "date": m.date,
        "location": m.location,
        "result": m.result
    } for m in matches])

@main_routes.route('/stats', methods=['GET'])
def get_stats():
    stats = scrape_stats()
    return jsonify(stats)

@main_routes.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([{
        "name": p.name,
        "role": p.role,
        "batting_style": p.batting_style,
        "bowling_style": p.bowling_style,
        "team": p.team
    } for p in players])

@main_routes.route('/add-player', methods=['POST'])
def add_player():
    data = request.get_json()
    new_player = Player(
        name=data.get("name"),
        role=data.get("role"),
        batting_style=data.get("batting_style"),
        bowling_style=data.get("bowling_style"),
        team=data.get("team", "UNSTOPPABLES CC")
    )
    db.session.add(new_player)
    db.session.commit()
    return jsonify({"status": "Player added"}), 201
