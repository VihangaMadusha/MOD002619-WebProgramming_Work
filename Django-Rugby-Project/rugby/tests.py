from django.test import TestCase

from .models import Player, Position


class RugbyModelTests(TestCase):
    def test_many_to_many_and_specialist(self):
        hooker = Position.objects.create(name="Hooker", specialist=True)
        wing = Position.objects.create(name="Left Wing")
        p = Player.objects.create(firstName="Jamie", lastName="George", age=33)
        p.positions.add(hooker, wing)
        self.assertEqual(p.positions.count(), 2)
        self.assertEqual(list(p.specialist_positions()), [hooker])
        self.assertEqual(hooker.player_set.count(), 1)
        self.assertEqual(str(p), "Jamie GEORGE")
