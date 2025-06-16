from .models import League, Player, Squad, Venue

def create_squad_service(
    name : str, 
    size: int, 
    league_id :int, 
    description: str,
    venue_id: int = None) -> Squad:
    
            try:
                league = League.objects.get(id=league_id)
            except (League.DoesNotExist, Venue.DoesNotExist):
                raise ValueError(f"League with id {league_id} does not exist.")
            home_venue = None
            if venue_id:
                try:
                    home_venue = Venue.objects.get(id=venue_id)
                except Venue.DoesNotExist:
                    raise ValueError(f"Venue with id {venue_id} does not exist.")
            squad = Squad.objects.create(
                name=name, 
                size=size, 
                description=description, 
                league=league, 
                home_venue=home_venue)   
            return squad

def retrieve_player_with_specific_age(age: int) -> Player:
    """
    Retrieve a player with a specific age.
    
    Args:
        age (int): The age of the player to retrieve.
        
    Returns:
        Player: The player with the specified age.
        
    Raises:
        ValueError: If no player with the specified age exists.
    """
    try:
        player = Player.objects.filter(age__gt = age)
        return list(player)
    except Player.DoesNotExist:
        raise ValueError(f"No player found with age {age}.")