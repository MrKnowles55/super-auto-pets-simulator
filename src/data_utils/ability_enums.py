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


class EffectTargetKind(Enum):
    AdjacentAnimals = 0
    AdjacentFriends = 1
    All = 2
    DifferentTierAnimals = 3
    EachEnemy = 4
    EachFriend = 5
    EachShopAnimal = 6
    FirstEnemy = 7
    FriendAhead = 8
    FriendBehind = 9
    HighestHealthEnemy = 10
    LastEnemy = 11
    LeftMostFriend = 12
    Level2And3Friends = 13
    LowestHealthEnemy = 14
    RandomEnemy = 15
    RandomFriend = 16
    RightMostFriend = 17
    Self = 18
    TriggeringEntity = 19
    LeftMostShopAnimal = 20

    TestTarget = 100


class TriggerByKind(Enum):
    Self = 0
    EachEnemy = 1
    EachFriend = 2
    FriendAhead = 3
    Player = 4

    TestTriggeredby = 100


class TriggerEvent(Enum):
    # ----- Outside Combat -----
    # Phase 0: Automatic Start
    StartOfTurn = 0
    UpgradeShopTier = 1

    # Phase 1: Player Initiated
    Buy = 2
    BuyAfterLoss = 3
    BuyFood = 4
    BuyTier1Animal = 5
    EatsShopFood = 6
    Sell = 7
    Roll = 8
    BuyAndSell = 9
    SpendGold = 10

    # Phase 0: Automatic End
    EndOfTurn = 11
    EndOfTurnWith2PlusGold = 12
    EndOfTurnWith4OrLessAnimals = 13
    EndOfTurnWithLvl3Friend = 14

    #  ----- Inside Combat -----
    # Phase 0: Before Fights
    CastsAbility = 15
    StartOfBattle = 16
    BeforeAttack = 17

    # Phase 1: During Fights
    EnemySummonedOrPushed = 18
    FriendAheadHurt = 19
    FriendHurt = 20
    EmptyFrontSpace = 21
    EnemySummoned = 22

    # Phase 2: After Fights
    KnockOut = 23
    AfterAttack = 24

    #  ----- Anytime -----
    # Phase 0:
    BeforeFaint = 25

    # Phase 1:
    Faint = 26
    Hurt = 27
    LevelUp = 28
    Summoned = 29
    AnyLevelUp = 30
    FriendLevelUp = 31
    HurtAndFaint = 32
    EndOfTurnAndStartOfBattle = 33

    # Test
    TestTrigger = 100