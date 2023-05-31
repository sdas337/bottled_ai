from typing import List

from rs.calculator.battle_state import BattleState
from rs.calculator.interfaces.comparator_interface import ComparatorInterface
from rs.common.comparators.common_general_comparator import Comparison, powers_we_like, powers_we_like_less, \
    powers_we_dislike, CommonGeneralComparator
from rs.common.comparators.core.assessment import ComparatorAssessmentConfig
from rs.common.comparators.core.comparisons import *

default_comparisons = [
    battle_not_lost,
    battle_is_won,
    most_optimal_winning_battle,
    most_free_early_draw,
    most_free_draw,
    most_lasting_intangible,
    least_incoming_damage_over_1,
    most_dead_monsters,
    most_enemy_vulnerable,
    most_enemy_weak,
    least_awkward_shivs,
    lowest_health_monster,
    lowest_total_monster_health,
    lowest_barricaded_block,
    most_draw_pay_early,
    most_draw_pay,
    most_good_player_powers,
    least_bad_player_powers,
    most_less_good_player_powers,
    least_enemy_artifacts,
    most_bad_cards_exhausted,
    least_incoming_damage,
    most_ethereal_cards_saved_for_later,
    most_energy,
]


class GeneralComparator(CommonGeneralComparator):

    def __init__(self, comparisons: List[Comparison] = None):
        super().__init__(default_comparisons if comparisons is None else comparisons)
