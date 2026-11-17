"""Run with:  python manage.py runscript load_players"""
from csv import DictReader

from rugby.models import Player, Position

POSITIONS = [
    ("Tight Head Prop", True), ("Hooker", True), ("Loose Head Prop", True), ("Second Row", True),
    ("Open Side Flanker", False), ("Blind Side Flanker", False), ("Number 8", False),
    ("Scrum Half", False), ("Fly Half", False), ("Inside Centre", False), ("Outside Centre", False),
    ("Left Wing", False), ("Right Wing", False), ("Full Back", False),
]


def run():
    if Player.objects.exists() or Position.objects.exists():
        print("Data already loaded...exiting. (Delete db.sqlite3 and re-run migrate to reload.)")
        return
    print("Creating positions")
    for name, specialist in POSITIONS:
        Position.objects.create(name=name, specialist=specialist)

    print("Loading players")
    with open("./players.csv") as fh:
        for row in DictReader(fh):
            player = Player.objects.create(firstName=row["fname"], lastName=row["lname"], age=row["age"])
            for pname in [n.strip() for n in row["positions"].split("| ") if n.strip()]:
                player.positions.add(Position.objects.get(name=pname))
    print("Done.")
