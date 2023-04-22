from enum import Enum


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
    EndOfTurnWith3PlusGold = 12
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
