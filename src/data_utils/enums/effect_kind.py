from enum import Enum


class EffectKind(Enum):
    AllOf = 0
    apply_status = 1
    deal_damage = 2
    discount_food = 3
    evolve = 4
    food_multiplier = 5
    gain_experience = 6
    gain_gold = 7
    modify_stats = 8
    OneOf = 9
    reduce_health = 10
    refill_shops = 11
    repeat_ability = 12
    summon_pet = 13
    summon_random_pet = 14
    swallow = 15
    transfer_ability = 16
    transfer_stats = 17
    roll_modifier = 18
    modify_shop = 19
    conserve_gold = 20
    steal_food = 21
    DamageAndModifyStats = 22
    gain_trumpets = 23
    MoveAndModifyStats = 24
    GainExperienceAndModifyStats = 25
    ApplyStatusAndModifyStats = 26
    move = 27
    KnockoutAndModifyStats = 28
    activate_ability = 29

    test_effect = 100