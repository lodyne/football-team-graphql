import strawberry


from djapps.team.types.graphgql_types import  DeleteItemResult
from djapps.team.types.django_types import LeagueType
from djapps.team.models import  League
    


@strawberry.type
class Mutation:
    

    @strawberry.mutation
    def create_league(self, name: str, country: str, description: str) -> LeagueType:
        """
        Create a new league.
        """
        league = League.objects.create(name=name,country=country, description=description)
        return league
    
    @strawberry.mutation
    def update_league(
        self,
        id: strawberry.ID,
        name: str = None,
        country: str = None,
        description: str = None
    ) -> LeagueType:
        """
        Update an existing league.
        """
        try:
            league = League.objects.get(id=id)
            if name is not None:
                league.name = name
            if country is not None:
                league.country = country
            if description is not None:
                league.description = description
            league.save()
            return league
        except League.DoesNotExist:
            raise ValueError(f"League with id {id} does not exist.")
    

    @strawberry.mutation
    def delete_league(self, id: strawberry.ID) -> DeleteItemResult:
        """
        Delete a league by ID.
        """
        try:
            league = League.objects.get(id=id)
            league.delete()
            message = f"League with id {id} has been deleted."
            return DeleteItemResult(success=True, message=message)
        except League.DoesNotExist:
            raise ValueError(f"League with id {id} does not exist.")
        
    

    