from enum import Enum


class TriggerEvent(Enum):
    AfterAttack = 0
    BeforeAttack = 1
    Buy = 2
    BuyAfterLoss = 3
    BuyFood = 4
    BuyTier1Animal = 5
    CastsAbility = 6
    EatsShopFood = 7
    EndOfTurn = 8
    EndOfTurnWith3PlusGold = 9
    EndOfTurnWith4OrLessAnimals = 10
    EndOfTurnWithLvl3Friend = 11
    Faint = 12
    Hurt = 13
    KnockOut = 14
    LevelUp = 15
    Sell = 16
    StartOfBattle = 17
    StartOfTurn = 18
    Summoned = 19
    EnemySummonedOrPushed = 20
    UpgradeShopTier = 21
    FriendAheadHurt = 22
    AnyLevelUp = 23
    FriendLevelUp = 24
    FriendHurt = 25
    EmptyFrontSpace = 26
    EnemySummoned = 27
    BeforeFaint = 28
    Roll = 29
    HurtAndFaint = 30
    EndOfTurnAndStartOfBattle = 31
    BuyAndSell = 32
    SpendGold = 33
