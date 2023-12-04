import json

exp_banned = [
    ['CSM1aC', '060'],
    ['CSM1aC', '128'],
    ['CSM1cC', '137'],
]
exp_banned_effect = []

with open('../output/sets_min.json', 'r') as f:
    contents = f.read()
    table = json.loads(contents)
    f.close()

for ban_card in exp_banned:
    found = False
    for coll in table:
        for card in coll['cards']:
            if card['collection_attr']['set_symbol'] == ban_card[0] and card['collection_attr']['card_no'] == ban_card[
                1]:
                exp_banned_effect.append(card['effect_id'])
                found = True
                break
        if found:
            break

with open('../output/banned.json', 'w') as f:
    f.write(json.dumps({
        'Standard': [],
        'Expanded': exp_banned_effect,
        'Sun & Moon Series': [],
    }, separators=(',', ':')))
