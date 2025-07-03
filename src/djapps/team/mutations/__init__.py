from .player.mutations import Mutation as PlayerMutation
from .coach.mutations import Mutation as CoachMutation
from .match.mutations import Mutation as MatchMutation
from .tournament.mutations import Mutation as TournamentMutation
from .player_tournament.mutations import Mutation as PlayerTournamentMutation
from .squad.mutations import Mutation as SquadMutation
from .league.mutations import Mutation as LeagueMutation  
import strawberry

@strawberry.type
class Mutation(PlayerMutation, CoachMutation,MatchMutation,
            TournamentMutation, PlayerTournamentMutation,
            SquadMutation, LeagueMutation):
    pass