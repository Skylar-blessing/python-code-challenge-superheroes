#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)

# Routes

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero is None:
        return make_response(jsonify(error="Hero not found"), 404)
    return jsonify(hero.to_dict())

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_update_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        return make_response(jsonify(error="Power not found"), 404)

    if request.method == 'PATCH':
        data = request.get_json()
        description = data.get('description')
        if not description or len(description) < 20:
            return make_response(jsonify(errors=["Invalid description"]), 400)
        power.description = description
        db.session.commit()
        return jsonify(power.to_dict())
    else:
        return jsonify(power.to_dict())

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not strength or strength not in ['Strong', 'Weak', 'Average']:
        return make_response(jsonify(errors=["Invalid strength"]), 400)

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None or power is None:
        return make_response(jsonify(error="Hero or Power not found"), 404)

    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero.to_dict())

if __name__ == '__main__':
    app.run(port=5555)
