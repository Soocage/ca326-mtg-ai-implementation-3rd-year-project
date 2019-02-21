import pickle
import sys
import card
import copy

cards = []

with open("../personal_decks/card_list.txt", "r") as f:
    n = f.readline()
    for i in range(int(n)):
        card_line = f.readline()
        card_line = card_line.strip()
        card_line = card_line.strip("[")
        card_line = card_line.strip("]")
        card_line = card_line.split(",")
        cards.append(card_line)

creatures = []
sorcs = []
insts = []
lnds = []

for c in cards:
    if c[1] == "Creature":
        crt = card.Creature(c[0], c[1], c[2], c[3],c[4],int(c[5]),int(c[6]))
        creatures.append(crt)

    elif c[1] == "Sorcery":
        c[5] = c[5].split(";")
        sor = card.Sorcery(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7])
        sorcs.append(sor)

    elif c[1] == "Instant":
        c[5] = c[5].split(";")
        insta = card.Instant(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7])
        insts.append(insta)

    elif c[1] == "Land":
        lnd = card.Land(c[0], c[1], c[2], c[3], c[4], c[5])
        lnds.append(lnd)

with open("../personal_decks/deck_info", "wb") as f:
    pickle.dump((len(creatures) + len(sorcs) + len(insts) + len(lnds)), f)
    for thing in creatures:
        pickle.dump(thing, f)

    for thing in sorcs:
        pickle.dump(thing, f)

    for thing in insts:
        pickle.dump(thing, f)

    for thing in lnds:
        pickle.dump(thing, f)

f = open("../personal_decks/deck_info", "rb")
n = pickle.load(f)
card_deck = []
for i in range(n):
    ver = pickle.load(f)
    with open("../personal_decks/deck_1", "wb") as deck_1:

        if ver.colour == "R" and ver.card_type == "Creature":
            for j in range(0,5):
                    tmp = copy.copy(ver)
                    card_deck.append(tmp)
                    

        if ver.colour == "R" and ver.card_type == "Sorcery":
            for j in range(0,2):
                    tmp = copy.copy(ver)
                    card_deck.append(tmp)
                   

        if ver.colour == "R" and ver.card_type == "Instant":
            for j in range(0,1):
                    tmp = copy.copy(ver)
                    card_deck.append(tmp)
                    

        if ver.colour == "R" and ver.card_type == "Land":
            for j in range(0,10):
                    tmp = copy.copy(ver)
                    card_deck.append(tmp)

        pickle.dump(card_deck, deck_1)
f.close()

f = open("../personal_decks/deck_info", "rb")
n = pickle.load(f)
card_deck = []
for i in range(n):
    ver = pickle.load(f)
    with open("../personal_decks/deck_2", "wb") as deck_2:
        if ver.colour == "B" and ver.card_type == "Creature":
            for j in range(0,5):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)
                    

        if ver.colour == "B" and ver.card_type == "Sorcery":
            for j in range(0,2):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                    

        if ver.colour == "B" and ver.card_type == "Instant":
            for j in range(0,1):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                    

        if ver.colour == "B" and ver.card_type == "Land":
            for j in range(0,10):
                tmp = copy.copy(ver)
                card_deck.append(tmp)

        pickle.dump(card_deck, deck_2)

f.close()

f = open("../personal_decks/deck_info", "rb")
n = pickle.load(f)
card_deck = []
for i in range(n):
    ver = pickle.load(f)
    with open("../personal_decks/deck_3", "wb") as deck_3:
        if ver.colour == "G" and ver.card_type == "Creature":
            for j in range(0,10):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(tmp)

        if ver.colour == "G" and ver.card_type == "Land":
            for j in range(0,10):
                tmp = copy.copy(ver)
                card_deck.append(tmp)

        if ver.colour == "G" and ver.card_type == "Instant":
            for j in range(0,1):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                    
        if ver.colour == "G" and ver.card_type == "Sorcery":
            for j in range(0,5):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
        
        pickle.dump(card_deck, deck_3)

f.close()

f = open("../personal_decks/deck_info", "rb")
n = pickle.load(f)
card_deck = []
for i in range(n):
    ver = pickle.load(f)
    with open("../personal_decks/deck_4", "wb") as deck_4:
        if ver.colour == "W" and ver.card_type == "Creature":
            for j in range(0,5):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)

        if ver.colour == "W" and ver.card_type == "Land":
            for j in range(0,15):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)

        if ver.colour == "W" and ver.card_type == "Instant":
            for j in range(0,1):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)
                
        if ver.colour == "W" and ver.card_type == "Sorcery":
            for j in range(0,5):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)
                

        pickle.dump(card_deck, deck_4)

f.close()

f = open("../personal_decks/deck_info", "rb")
n = pickle.load(f)
card_deck = []
for i in range(n):
    ver = pickle.load(f)
    with open("../personal_decks/deck_5", "wb") as deck_5:
        if ver.colour == "U" and ver.card_type == "Creature":
            for j in range(0,10):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)

        if ver.colour == "U" and ver.card_type == "Land":
            for j in range(0,10):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)

        if ver.colour == "U" and ver.card_type == "Instant":
            for j in range(0,1):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)
                
        if ver.colour == "U" and ver.card_type == "Sorcery":
            for j in range(0,5):
                tmp = copy.copy(ver)
                card_deck.append(tmp)
                print(ver.name)
                

        pickle.dump(card_deck, deck_5)

f.close()