from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.boss_relic_handler import BossRelicHandler


class BossRelicHandlerTestCase(RsTestHandlerFixture):
    handler = BossRelicHandler

    def test_select_first(self):
        self.execute_handler_tests('relics/boss_reward_first_is_best.json', ['choose 0'])

    def test_select_best(self):
        self.execute_handler_tests('relics/boss_reward_last_is_best.json', ['choose 2'])

    def test_skip_bad_energy_relics_when_applicable(self):
        self.execute_handler_tests('relics/boss_reward_nothing_to_take.json', ['skip', 'proceed'])

    def test_take_mark_of_pain(self):
        self.execute_handler_tests('relics/boss_reward_mark_of_pain.json', ['choose 1'])

    def test_take_coffee_dripper(self):
        self.execute_handler_tests('relics/boss_reward_coffee_dripper.json', ['choose 1'])

    def test_take_busted_crown(self):
        self.execute_handler_tests('relics/boss_reward_busted_crown.json', ['choose 1'])

    def test_calling_boss_relic_handler_multiple_games_in_a_row_does_not_break(self):
        self.execute_handler_tests('relics/boss_reward_double_run_bug_check.json', ['choose 2'])
        self.execute_handler_tests('relics/boss_reward_double_run_bug_check.json', ['choose 2'])
