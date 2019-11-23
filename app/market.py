from models import Set, Card
import random

def getPack(setName):
    cards = Card.query.filter_by(set='setName').all()
    pack = []
    while (i < 10):
        r = random.randint(0,len(cards))
        pack[i] = cards[r]
    return pack
