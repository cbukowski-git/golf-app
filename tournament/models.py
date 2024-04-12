from django.db import models
from django.contrib.auth.models import User


class Golfer(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to="golfers_photos/", blank=True, null=True
    )  # Optional image field

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to="tournaments_photos/", blank=True, null=True
    )  # Optional image field

    def __str__(self):
        return f"{self.name} on {self.date} at {self.location}"


class TournamentGolfer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE)
    total_score_to_par = models.IntegerField()  # Scores relative to par

    class Meta:
        unique_together = ("tournament", "golfer")

    def __str__(self):
        return f"{self.golfer.name} in {self.tournament.name} ({self.total_score_to_par} to par)"


class Payout(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("tournament", "position")

    def __str__(self):
        return (
            f"Position {self.position} payout ${self.amount} in {self.tournament.name}"
        )


class UserSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE)
    multiplier = models.PositiveSmallIntegerField()

    class Meta:
        # Ensure a golfer is not selected more than once per tournament by a user
        unique_together = ("user", "tournament", "golfer")

        # Ensure each multiplier 1-6 is used only once per user per tournament
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tournament", "multiplier"],
                name="unique_multiplier_per_tournament",
            )
        ]

    def __str__(self):
        return f"{self.user.username} selects {self.golfer.name} with multiplier {self.multiplier} for {self.tournament.name}"
