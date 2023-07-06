from models import db, Power, Hero, HeroPower
from random import choice, randint
from app import app

with app.app_context():
    print("🦸‍♀️ Seeding powers...")
    powers = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for power_data in powers:
        power = Power(**power_data)
        db.session.add(power)

    db.session.commit()
    print("🦸‍♀️ Powers seeded!")

    print("🦸‍♀️ Seeding heroes...")
    heroes = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for hero_data in heroes:
        hero = Hero(**hero_data)
        db.session.add(hero)

    db.session.commit()
    print("🦸‍♀️ Heroes seeded!")

    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]
    for hero in Hero.query.all():
        for _ in range(randint(1, 3)):
            # get a random power
            power = choice(Power.query.all())
            hero_power = HeroPower(strength=choice(strengths), hero=hero, power=power)
            db.session.add(hero_power)

    db.session.commit()
    print("🦸‍♀️ Powers added to heroes!")
    print("🦸‍♀️ Done seeding!")
