import strawberry

from djapps.team.types.django_types import PlayerType 

@strawberry.type
class SquadType:
    id: strawberry.ID
    name:str
    size:int
    description:str
    
@strawberry.type
class LeagueType:
    pass
    
@strawberry.type
class DeleteItemResult:
    success: bool
    message: str
    
@strawberry.type
class PlayerList:
    players: list['PlayerType']
    
@strawberry.type
class PlayerException:
    code: str
    message: str