from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.card_reward_handler import CardRewardHandler


class CardRewardHandlerTestCase(SgTestHandlerFixture):
    handler = CardRewardHandler

    def test_take_card(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_take.json', ['wait 30', 'choose 2', 'wait 30'])

    def test_snecko_skip(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_snecko_eye_skip.json', ['skip', 'proceed'])

    def test_snecko_eye_take_other(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_snecko_eye_take_other.json', ['wait 30', 'choose 1', 'wait 30'])

    def test_take_card_from_potion(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_potion_take.json', ['wait 30', 'choose 1', 'wait 30'])

    def test_take_card_from_potion_from_expanded_potion_list(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_potion_take_from_expanded_potion_list.json', ['wait 30', 'choose 1', 'wait 30'])

    def test_take_card_from_potion_prefer_original_deck_list(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_potion_prefer_original_deck_list.json', ['wait 30', 'choose 0', 'wait 30'])

    def test_forced_to_take_card_from_potion(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_potion_cannot_skip.json', ['wait 30', 'choose 0', 'wait 30'])
