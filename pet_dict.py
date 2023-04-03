from abilities import *

PET_DEFAULTS = {"Ant": {
    "attack": 2,
    "health": 1,
    "abilities": {
        "1": ModifyStatsAbility(attack_change=2, health_change=1, target='random_friendly', trigger_event='faint'),
        "2": ModifyStatsAbility(attack_change=4, health_change=2, target='random_friendly', trigger_event='faint'),
        "3": ModifyStatsAbility(attack_change=6, health_change=4, target='random_friendly', trigger_event='faint')
    },
    "tier": 1,
    "pack": "turtle"
},
    "Beaver": {
        "attack": 3,
        "health": 2,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=0, health_change=1, target='two_random_friendly',
                                    trigger_event='sell'),
            "2": ModifyStatsAbility(attack_change=0, health_change=2, target='two_random_friendly',
                                    trigger_event='sell'),
            "3": ModifyStatsAbility(attack_change=0, health_change=3, target='two_random_friendly',
                                    trigger_event='sell')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Cricket": {
        "attack": 1,
        "health": 2,
        "abilities": {
            "1": Summon(token='Zombie Cricket', trigger_event='faint'),
            "2": Summon(token='Zombie Cricket', trigger_event='faint'),
            "3": Summon(token='Zombie Cricket', trigger_event='faint')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Duck": {
        "attack": 2,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Fish": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=1, target='all_friends', trigger_event='level_up'),
            "2": ModifyStatsAbility(attack_change=2, health_change=2, target='all_friends', trigger_event='level_up'),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Horse": {
        "attack": 2,
        "health": 1,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=0, target='friend_summoned',
                                    trigger_event='friend_summoned'),
            "2": ModifyStatsAbility(attack_change=2, health_change=2, target='friend_summoned',
                                    trigger_event='friend_summoned'),
            "3": ModifyStatsAbility(attack_change=3, health_change=3, target='friend_summoned',
                                    trigger_event='friend_summoned')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Mosquito": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": Damage(damage=1, target='random_enemy', trigger_event='start_of_battle'),
            "2": Damage(damage=1, target='two_random_enemies', trigger_event='start_of_battle'),
            "3": Damage(damage=1, target='three_random_enemies', trigger_event='start_of_battle')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Pig": {
        "attack": 4,
        "health": 1,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Otter": {
        "attack": 1,
        "health": 2,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=1, target='random_friendly', trigger_event='buy'),
            "2": ModifyStatsAbility(attack_change=1, health_change=1, target='two_random_friendly',
                                    trigger_event='buy'),
            "3": ModifyStatsAbility(attack_change=1, health_change=1, target='three_random_friendly',
                                    trigger_event='buy')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Chinchilla": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": Summon(token='Loyal Chinchilla', trigger_event='sell'),
            "2": Summon(token='Loyal Chinchilla', trigger_event='sell'),
            "3": Summon(token='Loyal Chinchilla', trigger_event='sell')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Loyal Chinchilla": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Frilled Dragon": {
        "attack": 1,
        "health": 1,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=0, health_change=0, target="self", trigger_event="start_of_battle",
                                    scope="all_friends", filter="faint", attack_multiplier=1, health_multiplier=1),
            "2": ModifyStatsAbility(attack_change=0, health_change=0, target="self", trigger_event="start_of_battle",
                                    scope="all_friends", filter="faint", attack_multiplier=2, health_multiplier=2),
            "3": ModifyStatsAbility(attack_change=0, health_change=0, target="self", trigger_event="start_of_battle",
                                    scope="all_friends", filter="faint", attack_multiplier=3, health_multiplier=3)
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Marmoset": {
        "attack": 2,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Moth": {
        "attack": 2,
        "health": 1,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=3, health_change=0, target='front_most_friend',
                                    trigger_event='start_of_battle'),
            "2": ModifyStatsAbility(attack_change=6, health_change=0, target='front_most_friend',
                                    trigger_event='start_of_battle'),
            "3": ModifyStatsAbility(attack_change=9, health_change=0, target='front_most_friend',
                                    trigger_event='start_of_battle')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Beetle": {
        "attack": 2,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Bluebird": {
        "attack": 2,
        "health": 1,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=0, target='random_friend', trigger_event='end_turn'),
            "2": ModifyStatsAbility(attack_change=1, health_change=0, target='two_random_friends',
                                    trigger_event='end_turn'),
            "3": ModifyStatsAbility(attack_change=1, health_change=0, target='three_random_friends',
                                    trigger_event='end_turn')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Ladybug": {
        "attack": 1,
        "health": 3,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=2, health_change=0, target='self', trigger_event='shop_food_bought'),
            "2": ModifyStatsAbility(attack_change=4, health_change=0, target='self', trigger_event='shop_food_bought'),
            "3": ModifyStatsAbility(attack_change=6, health_change=0, target='self', trigger_event='shop_food_bought')
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Cockroach": {
        "attack": 1,
        "health": 4,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Duckling": {
        "attack": 1,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Frog": {
        "attack": 3,
        "health": 1,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Hummingbird": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Iguana": {
        "attack": 1,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Kiwi": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Mouse": {
        "attack": 2,
        "health": 1,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Pillbug": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Seahorse": {
        "attack": 2,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Sloth": {
        "attack": 1,
        "health": 1,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    "Zombie Cricket": {
        "attack": 1,
        "health": 1,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 1,
        "pack": "turtle"
    },
    # Tier 2
    "Crab": {
        "attack": 3,
        "health": 1,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=0, health_change=0, target="self", trigger_event="start_of_battle", scope="all_friends", get_best="health", health_multiplier=0.5),
            "2": ModifyStatsAbility(attack_change=0, health_change=0, target="self", trigger_event="start_of_battle", scope="all_friends", get_best="health", health_multiplier=1),
            "3": ModifyStatsAbility(attack_change=0, health_change=0, target="self", trigger_event="start_of_battle", scope="all_friends", get_best="health", health_multiplier=1.5)
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Dodo": {
        "attack": 3,
        "health": 3,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=0, health_change=0, target="friend_ahead", trigger_event="start_of_battle", scope="self", attack_multiplier=1/3),
            "2": ModifyStatsAbility(attack_change=0, health_change=0, target="friend_ahead", trigger_event="start_of_battle", scope="self", attack_multiplier=2/3),
            "3": ModifyStatsAbility(attack_change=0, health_change=0, target="friend_ahead", trigger_event="start_of_battle", scope="self", attack_multiplier=3/3),
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Elephant": {
        "attack": 3,
        "health": 5,
        "abilities": {
            "1": Damage(damage=1, target='friend_behind', trigger_event='before_attack'),
            "2": Damage(damage=2, target='friend_behind', trigger_event='before_attack'),
            "3": Damage(damage=3, target='friend_behind', trigger_event='before_attack'),
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Flamingo": {
        "attack": 4,
        "health": 2,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=1, target="2_friends_behind", trigger_event="faint"),
            "2": ModifyStatsAbility(attack_change=2, health_change=2, target="2_friends_behind", trigger_event="faint"),
            "3": ModifyStatsAbility(attack_change=3, health_change=3, target="2_friends_behind", trigger_event="faint"),
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Hedgehog": {
        "attack": 3,
        "health": 2,
        "abilities": {
            "1": Damage(damage=2, target='all', trigger_event='faint'),
            "2": Damage(damage=4, target='all', trigger_event='faint'),
            "3": Damage(damage=6, target='all', trigger_event='faint'),
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Peacock": {
        "attack": 2,
        "health": 5,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=4, health_change=0, target="self", trigger_event="hurt"),
            "2": ModifyStatsAbility(attack_change=8, health_change=0, target="self", trigger_event="hurt"),
            "3": ModifyStatsAbility(attack_change=12, health_change=0, target="self", trigger_event="hurt")
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Rat": {
        "attack": 4,
        "health": 5,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Shrimp": {
        "attack": 2,
        "health": 3,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=0, health_change=1, target="random_friend",
                                    trigger_event="friend_sold"),
            "2": ModifyStatsAbility(attack_change=0, health_change=2, target="random_friend",
                                    trigger_event="friend_sold"),
            "3": ModifyStatsAbility(attack_change=0, health_change=3, target="random_friend",
                                    trigger_event="friend_sold"),
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Spider": {
        "attack": 2,
        "health": 2,
        "abilities": {
            "1": Summon("tier_three_as_2_2", "faint"),
            "2": Summon("tier_three_as_4_4", "faint"),
            "3": Summon("tier_three_as_6_6", "faint")
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Swan": {
        "attack": 1,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Frigatebird": {
        "attack": 2,
        "health": 4,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Gold Fish": {
        "attack": 1,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Racoon": {
        "attack": 3,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Toucan": {
        "attack": 3,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Wombat": {
        "attack": 3,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "weekly"
    },
    "Bat": {
        "attack": 1,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "puppy"
    },
    "Dromedary": {
        "attack": 2,
        "health": 4,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "puppy"
    },
    "Tabby Cat": {
        "attack": 5,
        "health": 3,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=0, target="all_friends", trigger_event="eat_food"),
            "2": ModifyStatsAbility(attack_change=2, health_change=0, target="all_friends", trigger_event="eat_food"),
            "3": ModifyStatsAbility(attack_change=3, health_change=0, target="all_friends", trigger_event="eat_food"),
        },
        "tier": 2,
        "pack": "puppy"
    },
    "Atlantic Puffin": {
        "attack": 1,
        "health": 3,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "turtle"
    },
    "Dove": {
        "attack": 2,
        "health": 1,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "star"
    },
    "Guinea Pig": {
        "attack": 1,
        "health": 1,
        "abilities": {
            "1": Summon("Guinea Pig", "buy"),
            "2": Summon("Guinea Pig", "buy"),
            "3": Summon("Guinea Pig", "buy")
        },
        "tier": 2,
        "pack": "star"
    },
    "Jellyfish": {
        "attack": 2,
        "health": 3,
        "abilities": {
            "1": ModifyStatsAbility(attack_change=1, health_change=1, target="self", trigger_event="pet_level_up"),
            "2": ModifyStatsAbility(attack_change=2, health_change=2, target="self", trigger_event="pet_level_up"),
            "3": ModifyStatsAbility(attack_change=3, health_change=3, target="self", trigger_event="pet_level_up"),
        },
        "tier": 2,
        "pack": "star"
    },
    "Koala": {
        "attack": 1,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "star"
    },
    "Panda": {
        "attack": 2,
        "health": 4,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "star"
    },
    "Pug": {
        "attack": 5,
        "health": 2,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "star"
    },
    "Salamander": {
        "attack": 2,
        "health": 4,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "star"
    },
    "Stork": {
        "attack": 2,
        "health": 1,
        "abilities": {
            "1": Summon("level_one_prev_tier_pet", "faint"),
            "2": Summon("level_two_prev_tier_pet", "faint"),
            "3": Summon("level_three_prev_tier_pet", "faint")
        },
        "tier": 2,
        "pack": "star"
    },
    "Yak": {
        "attack": 3,
        "health": 5,
        "abilities": {
            "1": No_Ability(),
            "2": No_Ability(),
            "3": No_Ability()
        },
        "tier": 2,
        "pack": "star"
    },
}

TOKENS = [
    "Zombie Cricket",
    "Loyal Chinchilla"
]

BUYABLE = list(set(list(PET_DEFAULTS.keys())) - set(TOKENS))

# Tiers
TIER_1 = [key for key, value in PET_DEFAULTS.items() if value.get("tier") == 1]
TIER_2 = [key for key, value in PET_DEFAULTS.items() if value.get("tier") == 2]
TIER_3 = [key for key, value in PET_DEFAULTS.items() if value.get("tier") == 3]
TIER_4 = [key for key, value in PET_DEFAULTS.items() if value.get("tier") == 4]
TIER_5 = [key for key, value in PET_DEFAULTS.items() if value.get("tier") == 5]
TIER_6 = [key for key, value in PET_DEFAULTS.items() if value.get("tier") == 6]

# Abilities
HAS_FAINT_ABILITY = [key for key, value in PET_DEFAULTS.items() if value.get("abilities")["1"].trigger_event == "faint"]
HAS_SELL_ABILITY = [key for key, value in PET_DEFAULTS.items() if value.get("abilities")["1"].trigger_event == "sell"]
HAS_START_OF_BATTLE_ABILITY = [key for key, value in PET_DEFAULTS.items() if value.get("abilities")["1"].trigger_event == "start_of_battle"]


IMPLEMENTED = [  # For Level 1 at least
    "Ant",
    "Cricket",
    "Mosquito",
    "Moth",
    "Sloth",
    "Hedgehog",  # Fixed?? Error with Cricket
    "Elephant",
    "Peacock",
    "Flamingo",
    "Crab",
    "Frilled Dragon"
]

TEST_POOL = [
    "Frilled Dragon",
    "Cricket"
]

TEST_POOL2 = [
    "Cricket",
    "Hedgehog"
]

if __name__ == "__main__":
    pets = []
    # for k in PET_DEFAULTS.keys():
    #     pets.append(k)
    # for pet in (sorted(pets)):
    #     print(pet)
