import strawberry
from .match.queries import Query as MatchQuery
from .tournament.queries import Query as TournamentQuery        
from .player.queries import Query as PlayerQuery
from .coach.queries import Query as CoachQuery
from .league.queries import Query as LeagueQuery
from .squad.queries import Query as SquadQuery
from .venue.queries import Query as VenueQuery
from .player_tournament.queries import Query as PlayerTournamentQuery

@strawberry.type
class Query(MatchQuery, TournamentQuery, PlayerQuery,
            CoachQuery, LeagueQuery, SquadQuery,
            VenueQuery, PlayerTournamentQuery):
    pass