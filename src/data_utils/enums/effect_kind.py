from enum import Enum


class EffectKind(Enum):
    AllOf = 0
    ApplyStatus = 1
    DealDamage = 2
    DiscountFood = 3
    Evolve = 4
    FoodMultiplier = 5
    GainExperience = 6
    GainGold = 7
    ModifyStats = 8
    OneOf = 9
    ReduceHealth = 10
    RefillShops = 11
    RepeatAbility = 12
    SummonPet = 13
    SummonRandomPet = 14
    Swallow = 15
    TransferAbility = 16
    TransferStats = 17
    RollModifier = 18
    ModifyShop = 19
    ConserveGold = 20
    StealFood = 21
    DamageAndModifyStats = 22
    GainTrumpets = 23
    MoveAndModifyStats = 24
    GainExperienceAndModifyStats = 25
    ApplyStatusAndModifyStats = 26
    Move = 27
    KnockoutAndModifyStats = 28
    ActivateAbility = 29

    TestEffect = 100