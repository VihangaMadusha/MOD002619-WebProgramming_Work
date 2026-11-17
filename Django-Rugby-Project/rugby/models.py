from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # Specialist positions (front row / second row) are only played by players
    # who have been specifically allocated to them, for safety reasons.
    specialist = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name + (" (specialist)" if self.specialist else "")


class Player(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    age = models.IntegerField()
    # many players <-> many positions
    positions = models.ManyToManyField(Position, blank=True)

    class Meta:
        ordering = ["lastName", "firstName"]

    def __str__(self):
        return f"{self.firstName} {self.lastName.upper()}"

    def specialist_positions(self):
        return self.positions.filter(specialist=True)
