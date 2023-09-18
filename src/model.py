import hashlib
from enum import Enum
from typing import List, Optional


class Series(Enum):
    SM = 'Sun & Moon'
    SS = 'Sword & Shield'
    SV = 'Scarlet & Violet'


class SetType(Enum):
    MainExpansion = 0
    SideProduct = 1


class CardType(Enum):
    Pokemon = 'Pokemon'
    Trainer = 'Trainer'
    Energy = 'Energy'
    Item = 'Item'
    Supporter = 'Supporter'
    Stadium = 'Stadium'
    Tool = 'Pokemon Tool'
    BasicEnergy = 'Basic Energy'
    SpecialEnergy = 'Special Energy'


class Mechanic(Enum):
    ex = 'ex'
    V = 'V'
    GX = 'GX'
    Radiant = 'Radiant'
    Prism_Star = 'Prism Star'
    ACE_SPEC = 'ACE SPEC'


class Label(Enum):
    TAG_TEAM = 'TAG TEAM'
    Ultra_Beast = 'Ultra Beast'
    Fusion_Strike = 'Fusion Strike'
    Single_Strike = 'Single Strike'
    Rapid_Strike = 'Rapid Strike'


class Rarity(Enum):
    Common = 'C'
    Uncommon = 'U'
    Rare = 'R'
    PrismRare = 'PR'
    DoubleRare = 'RR'
    TripleRare = 'RRR'
    Shiny = 'S'
    SuperRare = 'SR'
    ShinySuperRare = 'SSR'
    CharacterRare = 'CHR'
    AmazingRare = 'A'
    HyperRare = 'HR'
    UltraRare = 'UR'
    NoLabel = ''


class Energy(Enum):
    Grass = 'G'
    Fire = 'R'
    Water = 'W'
    Lightning = 'L'
    Psychic = 'P'
    Fighting = 'F'
    Darkness = 'D'
    Metal = 'M'
    Fairy = 'Y'
    Dragon = 'N'
    Colorless = 'C'

    Zero = '0'
    Addition = '+'


class Stage(Enum):
    Basic = 'Basic'
    Stage1 = 'Stage 1'
    Stage2 = 'Stage 2'
    VMAX = 'VMAX'
    VSTAR = 'VSTAR'
    V_UNION = 'V-UNION'


class AncientTrait(Enum):
    Tera = 'Tera'


class Resistance:
    resistance_type: Energy
    resistance_value: str

    def __init__(self, resistance_type: Energy, resistance_value: str) -> None:
        self.resistance_type = resistance_type
        self.resistance_value = resistance_value

    def __json__(self):
        return {
            "resistance_type": self.resistance_type.value,
            "resistance_value": self.resistance_value
        }


class Weakness:
    weakness_type: Energy
    weakness_value: str

    def __init__(self, weakness_type: Energy, weakness_value: str) -> None:
        self.weakness_type = weakness_type
        self.weakness_value = weakness_value

    def __json__(self):
        return {
            "weakness_type": self.weakness_type.value,
            "weakness_value": self.weakness_value
        }


class Attack:
    name: str
    text: str
    cost: List[Energy]
    damage: Optional[str]

    def __init__(self,
                 name: str,
                 text: str,
                 cost: List[Energy],
                 damage: Optional[str]) -> None:
        self.name = name
        self.text = text
        self.cost = cost
        self.damage = damage

    def __json__(self):
        return {
            'name': self.name,
            'text': self.text,
            'cost': [energy.value for energy in self.cost],
            'damage': self.damage,
        }


class Ability:
    name: str
    text: str

    def __init__(self, name: str, text: str) -> None:
        self.name = name
        self.text = text

    def __json__(self):
        return {
            'name': self.name,
            'text': self.text,
        }


class PokemonAttr:
    energy_type: Energy
    stage: Stage
    hp: int
    ability: Optional[Ability]
    ancient_trait: Optional[AncientTrait]
    weakness: Optional[Weakness]
    resistance: Optional[Resistance]
    retreat_cost: int
    pokedex: str
    attacks: List[Attack]

    def __init__(self,
                 energy_type: Energy,
                 stage: Stage,
                 hp: int,
                 ability: Optional[Ability],
                 ancient_trait: Optional[AncientTrait],
                 weakness: Optional[Weakness],
                 resistance: Optional[Resistance],
                 retreat_cost: int,
                 pokedex: str,
                 attacks: List[Attack],
                 ):
        self.energy_type = energy_type
        self.stage = stage
        self.hp = hp
        self.ability = ability
        self.ancient_trait = ancient_trait
        self.weakness = weakness
        self.resistance = resistance
        self.retreat_cost = retreat_cost
        self.pokedex = pokedex
        self.attacks = attacks

    def __json__(self):
        return {
            'energy_type': self.energy_type.value,
            'stage': self.stage.value,
            'hp': self.hp,
            'ability': self.ability.__json__() if self.ability else None,
            'ancient_trait': self.ancient_trait.value if self.ancient_trait else None,
            'weakness': self.weakness.__json__() if self.weakness else None,
            'resistance': self.resistance.__json__() if self.resistance else None,
            'retreat_cost': self.retreat_cost,
            'pokedex': self.pokedex,
            'attacks': [attack.__json__() for attack in self.attacks]
        }


class EnergyAttr:
    energy: Energy

    def __init__(self, energy) -> None:
        self.energy = energy

    def __json__(self):
        return {
            "energy": self.energy.value
        }


class CollectionAttr:
    series: Series
    set_symbol: str
    # card_no / set_collect_num
    card_no: Optional[str]
    set_collect_num: Optional[str]
    artist_name: Optional[str]
    rarity: Rarity

    def __init__(self, series: Series, set_symbol: str, set_collect_num: str, card_no: str, artist_name: str,
                 rarity: Rarity) -> None:
        self.series = series
        self.set_symbol = set_symbol
        self.set_collect_num = set_collect_num
        self.card_no = card_no
        self.artist_name = artist_name
        self.rarity = rarity

    def __json__(self):
        return {
            'series': self.series.value,
            'set_symbol': self.set_symbol,
            'card_no': self.card_no,
            'set_collect_num': self.set_collect_num,
            'artist_name': self.artist_name,
            'rarity': self.rarity.value
        }


class Card:
    name: str
    text: str
    type: CardType
    mechanic: Mechanic
    label: Optional[Label]
    pokemon_attr: Optional[PokemonAttr]
    energy_attr: Optional[EnergyAttr]
    collection_attr: CollectionAttr
    regulation_mark: Optional[str]
    img_path: str
    effect_id: str

    def __init__(self,
                 name: str,
                 text: str,
                 ctype: CardType,
                 mechanic: Optional[Mechanic],
                 label: Optional[Label],
                 pokemon_attr: Optional[PokemonAttr],
                 collection_attr: CollectionAttr,
                 energy_attr: Optional[EnergyAttr],
                 regulation_mark: Optional[str],
                 ) -> None:
        self.name = name
        self.text = text
        self.type = ctype
        self.mechanic = mechanic
        self.label = label
        self.pokemon_attr = pokemon_attr
        self.collection_attr = collection_attr
        self.regulation_mark = regulation_mark
        self.energy_attr = energy_attr

        # EffectId
        if self.type == CardType.Pokemon:
            self.effect_id = (f"{self.name}|"
                              f"{self.pokemon_attr.stage.value}|"
                              f"{self.pokemon_attr.hp}|"
                              f"{self.pokemon_attr.ability.name if self.pokemon_attr.ability else ''}|"
                              f"{[attack.name for attack in self.pokemon_attr.attacks]}|"
                              f"{self.pokemon_attr.weakness.weakness_type if self.pokemon_attr.weakness else ''}|"
                              f"{self.pokemon_attr.weakness.weakness_value if self.pokemon_attr.weakness else ''}|"
                              f"{self.pokemon_attr.resistance.resistance_type.value if self.pokemon_attr.resistance else ''}|"
                              f"{self.pokemon_attr.resistance.resistance_value if self.pokemon_attr.resistance else ''}|"
                              f"{self.pokemon_attr.retreat_cost}")
        else:
            self.effect_id = f"{self.name}"
        self.effect_id = hashlib.md5(self.effect_id.encode()).hexdigest()

    def __json__(self):
        return {
            'name': self.name,
            'text': self.text,
            'type': self.type.value,
            'mechanic': self.mechanic.value if self.mechanic else None,
            'label': self.label.value if self.label else None,
            'pokemon_attr': self.pokemon_attr.__json__() if self.pokemon_attr else None,
            'collection_attr': self.collection_attr.__json__(),
            'energy_attr': self.energy_attr.__json__() if self.energy_attr else None,
            'regulation_mark': self.regulation_mark,
            'effect_id': self.effect_id
        }


class PSet:
    name: str
    symbol: str
    release_date: Optional[str]
    series: Series
    cards: List[Card]
    set_type: SetType
    cards_num: int

    def __init__(self, name: str, symbol: str, release_date: Optional[str],
                 series_id: Series) -> None:
        self.name = name
        self.symbol = symbol
        self.release_date = release_date
        self.series = series_id
        self.cards = []

        if symbol in [
            # SM
            'CSM1aC', 'CSM1bC', 'CSM1cC', 'CSM1.5C', 'CSM2aC', 'CSM2bC', 'CSM2cC', 'CSM2.5C',
            # SS
            'CS1aC', 'CS1bC', 'CS1.5C', 'CS2aC', 'CS2bC'
        ]:
            self.set_type = SetType.MainExpansion
        else:
            self.set_type = SetType.SideProduct

    def __json__(self):
        data = {
            'name': self.name,
            'symbol': self.symbol,
            'release_date': self.release_date,
            'series': self.series.value,
            'main_expansion': self.set_type == SetType.MainExpansion,
            'cards': [card.__json__() for card in self.cards],
            'cards_num': self.cards_num
        }
        if len(data['cards']) == 0:
            del data['cards']
        return data
