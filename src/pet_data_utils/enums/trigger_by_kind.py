from enum import Enum


class TriggerByKind(Enum):
    Self = 0
    EachEnemy = 1
    EachFriend = 2
    FriendAhead = 3
    Player = 4
