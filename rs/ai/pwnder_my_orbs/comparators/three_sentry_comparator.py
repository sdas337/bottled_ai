from rs.ai.pwnder_my_orbs.comparators.general_comparator import GeneralComparator, default_comparisons
from rs.common.comparators.common_general_comparator import add_to_comparison_list, move_in_comparison_list
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
comparisons.remove(lowest_health_monster)
add_to_comparison_list(comparisons, comparison_to_add=lowest_health_edge_monster, after=most_lasting_intangible)
move_in_comparison_list(comparisons, comparison_to_move=most_dead_monsters, after=most_lasting_intangible)


# Difference to normal comparator:
# Go very aggressive on killing either the front or back sentry for as long as there are 3 sentries alive.
class ThreeSentriesComparator(GeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
