import strawberry


from strawberry.types import Info

from djapps.team.models import League
from djapps.team.types.django_types import LeagueType
from djapps.team.utils import paginated_queryset


@strawberry.type
class Query:
    
        
    @strawberry.field
    def league_list(self, info:Info, order:str = None) -> list[LeagueType]:
        """
        Get all leagues.
        """
        queryset = League.objects.all()
        if order in ["id", "-id"]:  
            queryset = queryset.order_by(order)
        return queryset

    @strawberry.field
    def league_by_page(
        self,
        info : Info,
        limit: int = 0,
        offset: int = 0
    ) -> list[LeagueType]:
        
        """Get leagues with pagination. """
        queryset = League.objects.all().order_by("id")
        paginated_leagues = paginated_queryset(queryset, limit, offset)
        return paginated_leagues
        
    
    @strawberry.field
    def league_by_id(self,info : Info, id : strawberry.ID) -> LeagueType:
        try:
            league= League.objects.filter(id=id).first()
            return league
        except League.DoesNotExist:
            raise ValueError(f"League with id:{id} does not exist")
        
    