import unittest

from rs.machine.orb import Orb
from test_helpers.resources import load_resource_state


class MachineOrbsTest(unittest.TestCase):

    def test_orb_slot_count(self):
        state = load_resource_state("battles/with_orbs/basic_defect_with_orbs.json")
        count = state.get_player_orb_slots()
        self.assertEqual(3, count)

    def test_orb_slot_count_when_no_orbs(self):
        state = load_resource_state("battles/general/battle_simple_state.json")
        count = state.get_player_orb_slots()
        self.assertEqual(0, count)

    def test_get_orbs(self):
        state = load_resource_state("battles/with_orbs/basic_defect_with_orbs.json")
        orbs = state.get_player_orbs()
        self.assertEqual(1, len(orbs))
        (orbId, amount) = orbs[0]
        self.assertEqual(Orb.LIGHTNING, orbId)
        self.assertEqual(3, amount)

    # TODO -> still need to add coverage for the other types. Specifically plasma, when we see it.
