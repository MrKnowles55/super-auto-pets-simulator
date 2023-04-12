from enum import Enum


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