from datetime import datetime
from typing import Optional
from ..models import (
    Coach, 
    Player, 
    PlayerMatch, 
    PlayerTournament, 
    Squad, 
    League, 
    Match, 
    SquadTournament, 
    Tournament, 
    Venue
)
import strawberry
import strawberry.django



@strawberry.django.type(League)  
class LeagueType:
    id: strawberry.ID
    name: str
    country: str
    description: str    

@strawberry.django.type(Squad)
class SquadType:
    id: strawberry.ID
    name:str
    size:int
    description:str
    league: LeagueType
    home_venue: Optional["VenueType"] = strawberry.django.field()
    
    
@strawberry.django.type(Coach)
class CoachType:
    id:strawberry.ID
    name: str
    squad: SquadType
    
@strawberry.django.type(Player)
class PlayerType:
    id: strawberry.ID
    name:str
    squad : SquadType
    position: str
    age : int
    nationality: str
    
@strawberry.django.type(Match)
class MatchType:
    id: strawberry.ID
    home_team : SquadType
    away_team : SquadType
    date : datetime
    venue : 'VenueType'
    score_home : int
    score_away : int
    
@strawberry.django.type(Venue)
class VenueType:
    id: strawberry.ID
    name: str
    location: str
    capacity: int
    matches: list[MatchType] = strawberry.django.field()
    
    
@strawberry.django.type(PlayerMatch)
class PlayerMatchType:
    player: PlayerType
    match: MatchType
    goals: int
    assists: int
    
@strawberry.django.type(Tournament)
class TournamentType:
    id: strawberry.ID
    name: str
    description: str
    squads: list[SquadType] = strawberry.django.field()
    teams: list[MatchType] = strawberry.django.field()
    
@strawberry.django.type(SquadTournament)
class SquadTournamentType:
    squad: SquadType
    tournament: TournamentType
    
@strawberry.django.type(PlayerTournament)
class PlayerTournamentType:
    id: strawberry.ID
    player: PlayerType
    tournament: TournamentType
    goals: int
    assists: int