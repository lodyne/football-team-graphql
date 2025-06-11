from django.db import models

# Base model to include common fields like created_at and updated_at

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Models for the team application

class League(BaseModel):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "league"
        verbose_name = "League"
        verbose_name_plural = "Leagues"
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name
    
class Squad(BaseModel):
    name = models.CharField(max_length=50)
    size = models.IntegerField(default=0)
    league = models.ForeignKey(
        League,
        related_name='squads',
        on_delete=models.CASCADE) 
    home_venue = models.ForeignKey(
        'Venue',
        related_name='home_squads',
        on_delete=models.CASCADE,
        blank=True,
        null=True)  
    description = models.TextField(blank=True, null=True)

    
    class Meta:
        db_table = "squad"
        verbose_name = "Squad"
        verbose_name_plural = "Squads"
        ordering = ["-created_at"]
        
class Coach(BaseModel):
    name = models.CharField(max_length=50)
    squad = models.OneToOneField(
        Squad, 
        related_name='coach', 
        on_delete=models.CASCADE,
        unique=True) # Assuming a coach can only be associated with one squad at a time
    
    class Meta:
        db_table = "coach"
        verbose_name = "Coach"
        verbose_name_plural = "Coaches"
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name
    
class Player(BaseModel):
    name = models.CharField(max_length=50)
    squad = models.ForeignKey(
        Squad, 
        related_name='players', 
        on_delete=models.CASCADE
        )
    position = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)
    player_match = models.ManyToManyField(
        'Match', 
        through='PlayerMatch', 
        related_name='players')
    
    class Meta:
        db_table = "player"
        verbose_name = "Player"
        verbose_name_plural = "Players"
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name

class Match(BaseModel):
    home_team = models.ForeignKey(
        Squad, 
        related_name='home_matches', 
        on_delete=models.CASCADE
        )
    away_team = models.ForeignKey(
        Squad, 
        related_name='away_matches', 
        on_delete=models.CASCADE
        )
    date = models.DateTimeField()
    venue = models.ForeignKey(
        'Venue',
        related_name='matches',
        on_delete=models.CASCADE)
    score_home = models.IntegerField(default=0)
    score_away = models.IntegerField(default=0)

    class Meta:
        db_table = "match"
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        ordering = ["-date"]
        
    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.date} at {self.venue.name}"

class PlayerMatch(BaseModel):
    player = models.ForeignKey(
        Player, 
        related_name='player_matches',
        on_delete=models.CASCADE
        )
    match = models.ForeignKey(
        Match, 
        related_name='match_players', 
        on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    class Meta:
        db_table = "player_match"
        verbose_name = "Player Match"
        verbose_name_plural = "Player Matches"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.player.name} in {self.match}"
    
class Tournament(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    teams = models.ManyToManyField(
        Player, 
        related_name='team_tournaments',
        through='PlayerTournament',
        )
    squad = models.ManyToManyField(
        Squad, 
        related_name='squad_tournaments',
        through='SquadTournament',
        )

    class Meta:
        db_table = "tornament"
        verbose_name = "Tornament"
        verbose_name_plural = "Tornaments"
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name
    
class PlayerTournament(BaseModel):
    player = models.ForeignKey(
        Player, 
        related_name='player_tournaments', 
        on_delete=models.CASCADE
        )
    tornament = models.ForeignKey(
        Tournament, 
        related_name='tournament_players', 
        on_delete=models.CASCADE
        )
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    class Meta:
        db_table = "player_tournament"
        verbose_name = "Player Tournament"
        verbose_name_plural = "Player Tournaments"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.player.name} in {self.tornament}"
    
class Venue(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(default=0)

    class Meta:
        db_table = "venue"
        verbose_name = "Venue"
        verbose_name_plural = "Venues"
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name
    
class SquadTournament(BaseModel):
    squad = models.ForeignKey(
        Squad, 
        related_name='squad_tornaments', 
        on_delete=models.CASCADE
        )
    tournament = models.ForeignKey(
        Tournament, 
        related_name='tornament_squads', 
        on_delete=models.CASCADE
        )

    class Meta:
        db_table = "squad_tournament"
        verbose_name = "Squad Tournament"
        verbose_name_plural = "Squad Tournaments"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.squad.name} in {self.tournament.name}"
    
    