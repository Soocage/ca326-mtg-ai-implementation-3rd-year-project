import pickle
import sys
import card

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
inst = []

for c in cards:
    if c[1] == "Creature":
        crt = card.Creature(c[0], c[1], c[2], c[3],c[4],int(c[5]),int(c[6]))
        creatures.append(crt)

    elif c[1] == "Sorcery":
        c[5] = c[5].split(";")
        print (c)
        sor = card.Sorcery(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7])
        sorcs.append(sor)

    else:
        inst.append(c)

with open("../personal_decks/deck_info", "wb") as f:
    pickle.dump((len(creatures)+len(sorcs)), f)
    for thing in creatures:
        pickle.dump(thing, f)
    for thing in sorcs:
        pickle.dump(thing, f)

f = open("../personal_decks/deck_info", "rb")
n = pickle.load(f)
for i in range(n):
    ver = pickle.load(f)
    print(ver.name)
f.close()

