import strawberry


from djapps.team.types.graphgql_types import  DeleteItemResult, FieldError, LeagueResponse
from djapps.team.types.django_types import LeagueType
from djapps.team.models import  League
    


@strawberry.type
class Mutation:
    

    @strawberry.mutation
    def create_league(self, name: str, country: str, description: str) -> LeagueResponse:
        """
        Create a new league.
        """
        existing = League.objects.filter(name=name, country=country).first()
        
        if existing:
            return LeagueResponse(
                ok=False,
                message=f"A league named {name} already exists in {country}.",
                league=LeagueType(
                    id=existing.id,
                    name=existing.name,
                    country=existing.country,
                    description=existing.description  
                ) ,
                errors=[FieldError(field="name", message=f"{name}, already exists.")]
            )
            # raise ValueError(f"League with name {name} in country {country} already exists.")
        league = League.objects.create(name=name,country=country, description=description)
        
        response = LeagueResponse(
            ok=True,
            message=f"{league.name}  created successfully.",
            league=LeagueType(
                id=league.id,
                name=league.name,
                country=league.country,
                description=league.description
            ),
            errors=[]
        )
        
        return response
    
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
        
    

    