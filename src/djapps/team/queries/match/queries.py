import strawberry

from strawberry.types import Info

from djapps.team.models import Match
from djapps.team.types.django_types import MatchType


@strawberry.type
class Query:
    
    @strawberry.field
    def match_list(self, info: Info) -> list['MatchType']:
        """
        Get all matches.
        """
        return Match.objects.all()
    
    @strawberry.field
    def match_by_id(self, info: Info, id: strawberry.ID) -> list['MatchType']:
        """
        Get all matches.
        """
        try:
            match = Match.objects.filter(id=id).first() 
            return match
        except Match.DoesNotExist:
            raise ValueError(f"Match with id {id} does not exist.")
    
    