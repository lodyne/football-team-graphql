import strawberry

from djapps.team.types.django_types import CoachType, LeagueType, PlayerType 

@strawberry.type
class SquadType:
    id: strawberry.ID
    name:str
    size:int
    description:str
    
    
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
    
@strawberry.type
class CoachResponse:
    ok: bool
    message: str
    coach: CoachType | None

@strawberry.type
class FieldError:
    field: str
    message: str
    
@strawberry.type
class LeagueResponse:
    ok: bool
    message: str
    league: LeagueType | None
    errors: list[FieldError] | None = None