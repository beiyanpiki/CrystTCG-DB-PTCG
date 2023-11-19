import json
import shutil
from pathlib import Path
from typing import Optional, Tuple, Dict

from src.model import PSet, Series, Label, CardType, Mechanic, CollectionAttr, Rarity, PokemonAttr, Energy, Stage, \
    Ability, Resistance, Attack, Card, EnergyAttr

raw_json_path = '../PTCG-CHS-Datasets/ptcg_chs_infos.json'

with open(raw_json_path, 'r') as f:
    contents = f.read()
    table = json.loads(contents)
    collections = table['collections']
    collections.reverse()
    f.close()


def get_series(series_id: str, set_name: str) -> Series:
    match set_name:
        case '特典卡·太阳&月亮':
            series_id = '1'
        case '2023宝可梦卡牌大师赛·广州 特典':
            series_id = '1'
        case '宝可梦卡牌超级赛·太阳&月亮 特典':
            series_id = '1'
        case '特典卡·剑&盾':
            series_id = '2'
        case '宝可梦卡牌超级赛·剑&盾 特典':
            series_id = '2'
        case '2023宝可梦卡牌大师赛·北京 特典':
            series_id = '2'
        case '2023宝可梦卡牌大师赛·深圳 特典':
            series_id = '2'

    if series_id == '1':
        return Series.SM
    elif series_id == '2':
        return Series.SS
    elif series_id == '3':
        return Series.SV


def get_card_type(card) -> CardType:
    if card['cardType'] == '1':
        return CardType.Pokemon
    elif card['cardType'] == '2':
        if card['details']['trainerType'] == '1':
            if card['details']['ruleText'].startswith('宝可梦道具可以附着在自己的宝可梦身上'):
                return CardType.Tool
            else:
                return CardType.Item
        elif card['details']['trainerType'] == '2':
            return CardType.Supporter
        elif card['details']['trainerType'] == '3':
            return CardType.Stadium
    elif card['cardType'] == '3':
        if card['energyType'] == '1':
            return CardType.BasicEnergy
        elif card['energyType'] == '2':
            return CardType.SpecialEnergy

    print('wtf??? No such card type')
    exit(1)


def get_mechanic(card) -> Optional[Mechanic]:
    pt = [x for x in card.get('pokemonType', '').split('|') if x != '']
    # V: only pokemon has V mechanic
    if '1' in pt:
        return Mechanic.V

    # GX: only pokemon has GX mechanic
    if '4' in pt:
        return Mechanic.GX

    # Prism_Star: All card can have Prism Star mechanic
    if card.get('specialCard', None) == '4':
        return Mechanic.Prism_Star

    # Other mechanic(ex, Radiant, ACE SPEC) not in CHS card yet
    return None


def get_label(card) -> Optional[Label]:
    # TAG TEAM: Pokemon and Supporter card can have TAG TEAM
    if card.get('specialCard', None) == '5':
        return Label.TAG_TEAM

    # Ultra Beast: Only Pokemon has Ultra Beast
    pt = [x for x in card.get('pokemonType', '').split('|') if x != '']
    if '5' in pt:
        return Label.Ultra_Beast

    return None


def get_rarity(card) -> Rarity:
    rarity = card['details']['rarityText'].replace("☆", "")
    match rarity:
        case 'C':
            return Rarity.Common
        case 'U':
            return Rarity.Uncommon
        case 'R':
            return Rarity.Rare
        case 'PR':
            return Rarity.PrismRare
        case 'RR':
            return Rarity.DoubleRare
        case 'RRR':
            return Rarity.TripleRare
        case 'S':
            return Rarity.Shiny
        case 'SR':
            return Rarity.SuperRare
        case 'SSR':
            return Rarity.ShinySuperRare
        case 'CSR':
            return Rarity.CharacterSuperRare
        case 'CHR':
            return Rarity.CharacterRare
        case 'A':
            return Rarity.AmazingRare
        case 'HR':
            return Rarity.HyperRare
        case 'UR':
            return Rarity.UltraRare
        case '无标记':
            return Rarity.NoLabel
        case '_':
            input('WTF???')
            exit(1)


def get_card_in_coll(card) -> Tuple[str | None, str | None]:
    coll_no = card['details']['collectionNumber'].split('/')
    if len(coll_no) == 2:
        return coll_no[0], coll_no[1]
    else:
        if coll_no[0] in ['DAR', 'FAI', 'FIG', 'FIR', 'GRA', 'LIG', 'MET', 'PSY', 'WAT']:
            return coll_no[0], None
        elif coll_no[0] in ['SM-P', 'S-P']:
            return None, coll_no[0]
        else:
            return None, None


def get_energy_by_eid_yorenid(eid: str) -> Energy:
    match eid:
        case '1' | 'Y457' | 'Y755':
            return Energy.Grass
        case '2' | 'Y458' | 'Y756':
            return Energy.Fire
        case '3' | 'Y459':
            return Energy.Water
        case '4' | 'Y460' | 'Y757':
            return Energy.Lightning
        case '5' | 'Y461' | 'Y758':
            return Energy.Psychic
        case '6' | 'Y462' | 'Y759':
            return Energy.Fighting
        case '7' | 'Y463' | 'Y760':
            return Energy.Darkness
        case '8' | 'Y464':
            return Energy.Metal
        case '9' | 'Y465':
            return Energy.Fairy
        case '10':
            return Energy.Dragon
        case '11':
            return Energy.Colorless
        case 'none':
            return Energy.Zero
        case '12':
            return Energy.Addition
        case _:
            print("Error: Not valid eid or yorenId")
            print(eid)
            exit(1)


def get_stage(card) -> Stage:
    match card['details']['evolveText']:
        case '基础':
            return Stage.Basic
        case '1阶进化':
            return Stage.Stage1
        case '2阶进化':
            return Stage.Stage2
        case 'V进化':
            return Stage.VMAX
        case _:
            print('wtf????')
            exit(1)


def get_pokemon_attr(card) -> PokemonAttr:
    assert card['cardType'] == '1'

    energy_type = card['details']['attribute']
    energy_type = get_energy_by_eid_yorenid(energy_type)
    stage = get_stage(card)
    hp = card['details']['hp']

    ability = (card['details'].get('featureName', None), card['details'].get('featureText', None))
    if ability[0] is not None:
        ability = Ability(ability[0], ability[1])
    else:
        ability = None
    ancient_trait = None

    weakness_type = card['details'].get('weaknessType', None)
    if weakness_type is not None:
        weakness = get_energy_by_eid_yorenid(weakness_type)
    else:
        weakness = None

    resistance = (card['details'].get('resistanceType', None), card['details'].get('resistanceFormula', None))
    if resistance[0] is not None:
        resistance = Resistance(get_energy_by_eid_yorenid(resistance[0]), resistance[1])
    else:
        resistance = None

    retreat_cost = card['details'].get('retreatCost', 0)
    pokedex = card['details'].get('yorenCode', None)

    attacks = []
    for attack in card['details']['abilityItemList']:
        atk_name = "" if attack['abilityName'] =='none' else attack['abilityName']
        atk_text = "" if attack['abilityText'] == 'none' else attack['abilityText']
        atk_damage = "" if attack['abilityDamage'] == 'none' else attack['abilityDamage']

        if atk_name=="" and atk_text=="" and atk_damage=="":
            continue

        atk_cost = attack.get('abilityCost', '')
        atk_cost = ['none'] if atk_cost == '' else [elem for elem in atk_cost.split(',') if elem != ""]
        for i in range(len(atk_cost)):
            e = get_energy_by_eid_yorenid(atk_cost[i])
            atk_cost[i] = e

        atk = Attack(atk_name, atk_text, atk_cost, atk_damage)
        attacks.append(atk)
    return PokemonAttr(energy_type, stage, hp, ability, ancient_trait, weakness, resistance, retreat_cost, pokedex,
                       attacks)


def get_card_text(card, card_type) -> str:
    res = ''
    if card_type == CardType.Pokemon:
        if 'featureName' in card['details']:
            res += f"{card['details']['featureName']}\n{card['details']['featureText']}\n"
        for attack in card['details']['abilityItemList']:
            if 'abilityText' in attack:
                res += f"{attack['abilityName']}\t{attack['abilityDamage'] if attack['abilityDamage'] != 'none' else ''}\n{attack['abilityText'] if attack['abilityText'] != 'none' else ''}\n"
    elif card_type != CardType.BasicEnergy:
        r = card['details']['ruleText']
        r = r.replace("在自己的回合可以使用任意张物品卡。", '')
        r = r.replace('宝可梦道具可以附着在自己的宝可梦身上。每只宝可梦身上只可以附着1张宝可梦道具，并保持附加状态。', '')
        r = r.replace('在自己的回合只可以使用1张支援者卡。', '')
        r = r.replace(
            '在自己的回合只可以将1张竞技场卡放到战斗区旁。如果有别的名称的竞技场卡被放入场上，则将此卡放入弃牌区。', '')
        r = r.replace('在1副卡组中只能放入1张同名的◇（棱镜之星）卡。这张卡牌不会被放入弃牌区，而会被放入放逐区。', '')
        r = r.replace('在自己的回合只可以使用1张支援者卡', '')
        r = r.replace('|', '')
        res += f"{r}\n"
    else:
        res = ''
    return res


effect_dic = []


def sort_cards_by_card_no(card: Card):
    card_no = card.collection_attr.card_no
    if card_no.isdigit():
        return 0, int(card_no)
    elif card_no.startswith("NaN"):
        return 1, int(card_no[3:])
    else:
        return 2, card_no


def fix_card(database: Dict[str, PSet]):
    # SSP-138
    for (i, c) in enumerate(database['SSP'].cards):
        if c.collection_attr.card_no == '138':
            database['SSP'].cards[i].pokemon_attr.attacks[0].cost = [Energy.Colorless]
            break
    return database


def main():
    database = {}
    for collection in collections:
        set_name = collection['name']
        set_symbol = collection['commodityCode']
        set_publish_date = collection['salesDate']
        set_series_id = collection.get('series', None)
        set_series = get_series(set_series_id, set_name)

        sets = PSet(set_name, set_symbol, set_publish_date, set_series)

        for card in collection['cards']:
            if card['details']['rarityText'].find('☆') != -1:
                continue

            name = card['name']
            card_type = get_card_type(card)
            card_text = get_card_text(card, card_type)
            mechanic = get_mechanic(card)
            label = get_label(card)

            if card_type == CardType.BasicEnergy and name.find('【') != -1:
                name = name.replace('【','').replace('】','')




            card_idx, coll_num = get_card_in_coll(card)
            artist = card['details'].get('illustratorName', [None])[0]
            rarity = get_rarity(card)
            collect_attr = CollectionAttr(set_series, set_symbol, coll_num, card_idx, artist, rarity)
            regulation_mark = card['details'].get('regulationMarkText', None)
            pokemon_attr = get_pokemon_attr(card) if card_type == CardType.Pokemon else None
            energy_attr = EnergyAttr(
                get_energy_by_eid_yorenid(card['details']['yorenCode'])
            ) if card_type == CardType.BasicEnergy else None

            card_after = Card(name, card_text, card_type, mechanic, label, pokemon_attr, collect_attr, energy_attr,
                              regulation_mark)
            card_after.img_path = card['image']
            sets.cards.append(card_after)
        database[set_symbol] = sets

    database["SMP"] = database.pop("PROMO")
    database['SSP'] = database.pop("PROMO3")
    database['PROMO-MARNIE'] = database.pop("PROMO5")
    database['PROMO-CharizardA'] = database.pop("PROMO7")
    database['PROMO-CharizardB'] = database.pop("PROMO8")
    database['PROMO-1stA'] = database.pop("PROMO10")
    database['PROMO-1stB'] = database.pop("PROMO11")

    # Combine PROMO
    cnt = 0
    for k, v in database.items():
        if k in ['PROMO1', 'PROMO2']:
            for card in v.cards:
                c = card
                c.collection_attr.set_symbol = 'SMP'
                if c.collection_attr.card_no is None:
                    cnt += 1
                    c.collection_attr.card_no = f'NaN{cnt}'
                database['SMP'].cards.append(c)

    cnt = 0
    for k, v in database.items():
        if k in ['PROMO4', 'PROMO6', 'PROMO9', 'PROMO-CharizardA', 'PROMO-CharizardB', 'PROMO-1stA', 'PROMO-1stB']:
            for card in v.cards:
                c = card
                c.collection_attr.set_symbol = 'SSP'
                if c.collection_attr.card_no is None:
                    cnt += 1
                    c.collection_attr.card_no = f'NaN{cnt}'
                database['SSP'].cards.append(c)

    del database['PROMO1']
    del database['PROMO2']
    del database['PROMO4']
    del database['PROMO6']
    del database['PROMO9']

    for k, v in database.items():
        if database[k].symbol.find('PROMO') != -1:
            database[k].symbol = 'PROMO'
            for i in range(len(database[k].cards)):
                if database[k].series == Series.SM:
                    database[k].cards[i].collection_attr.set_symbol = 'SMP'
                elif database[k].series == Series.SS:
                    database[k].cards[i].collection_attr.set_symbol = 'SSP'
        database[k].cards_num = len(v.cards)

    database["SSP"].symbol = 'SSP'
    database["SSP"].set_id = 'SSP'
    database["SSP"].name = "剑&盾 特典卡"
    database['SSP'].release_date = None

    database["SMP"].symbol = 'SMP'
    database["SMP"].set_id = 'SMP'
    database["SMP"].name = '太阳&月亮 特典卡'
    database['SMP'].release_date = None

    database['PROMO-MARNIE'].set_id = 'PROMO-MARNIE'
    database['PROMO-CharizardA'].set_id = 'PROMO-CharizardA'
    database['PROMO-CharizardB'].set_id = 'PROMO-CharizardB'
    database['PROMO-1stA'].set_id = 'PROMO-1stA'
    database['PROMO-1stB'].set_id = 'PROMO-1stB'

    for k, v in database.items():
        if k in ['CSMPaC', 'CSMPbC', 'CSMPcC', 'CSMPdC', 'CSMPeC', 'CSMPfC', 'CSMPgC', 'CSMPhC']:
            database[k].cards = [c for c in database[k].cards if
                                 not (c.type == CardType.BasicEnergy and c.regulation_mark == 'C')]

    for k, v in database.items():
        if k == 'SMP':
            # PROMO has overlap cards
            database[k].cards = [c for c in database[k].cards if c.collection_attr.card_no is not None]
        if v.name.find('强化包') != -1:
            database[k].name = database[k].name[4:]
        if v.name.find('补充包') != -1:
            database[k].name = database[k].name[4:]
        database[k].cards = sorted(database[k].cards, key=sort_cards_by_card_no)

        # Fix error
    database = fix_card(database)

    return database


def custom_encoder(obj):
    if hasattr(obj, '__json__'):
        return obj.__json__()
    else:
        raise TypeError(f'Object of type {type(obj)} is not JSON serializable')


def convert_to_json(obj, compress=False):
    return json.dumps(obj, default=custom_encoder, indent=4) if not compress else json.dumps(obj,
                                                                                             default=custom_encoder,
                                                                                             separators=(',', ':'))


if __name__ == '__main__':
    data = main()

    sets = []
    for k, v in data.items():
        for card in v.cards:
            src = f'../PTCG-CHS-Datasets/{card.img_path}'.replace('\\', '/')
            dst = f'../output/img/{card.collection_attr.set_symbol}/{card.collection_attr.card_no}.jpg'.replace('\\', '/')
            folder = Path(f'../output/img/{card.collection_attr.set_symbol}'.replace('\\', '/'))
            folder.mkdir(parents=True, exist_ok=True)
            if Path(dst).is_file():
                print(f"{card.collection_attr.set_symbol}-{card.collection_attr.card_no}: This file is exist, please check the data")
                continue
            shutil.copy2(src, dst)
        sets.append(v)

    with open('../output/sets.json', 'w') as f:
        f.write(convert_to_json(sets))

    with open('../output/sets_min.json', 'w') as f:
        f.write(convert_to_json(sets, compress=True))
