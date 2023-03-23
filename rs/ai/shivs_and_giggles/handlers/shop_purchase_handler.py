from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.card import CardType
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class ShopPurchaseHandler(Handler):

    def __init__(self):
        self.relics = [
            'Shuriken',
            'Kunai',
            'Preserved Insect',
            'Ornamental Fan',
            'Bag of Marbles',
            'Vajra',
            'Molten Egg',
            'Meal Ticket',
            'Bronze Scales',
            'Orichalcum',
            'Anchor',
            'Horn Cleat',
        ]

        self.cards = [
            "Accuracy",
            "Blade Dance",
            "Escape Plan",
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.SHOP_SCREEN.value

    def handle(self, state: GameState) -> List[str]:
        choice = self.find_choice(state)
        if choice:
            idx = state.get_choice_list().index(choice)
            if presentation_mode:
                return [p_delay, "choose " + str(idx), p_delay_s, "wait 30"]
            return ["choose " + str(idx), "wait 30"]
        if presentation_mode:
            return ["wait " + p_delay, "return", "proceed"]
        return ["return", "proceed"]

    def find_choice(self, state: GameState) -> str:
        gold = state.game_state()['gold']
        screen_state = state.game_state()['screen_state']
        can_purge = screen_state['purge_available'] and gold >= screen_state['purge_cost']

        # 1. Purge curses
        if can_purge and state.deck.contains_type(CardType.CURSE):
            return "purge"

        # 2. Shuriken
        for relic in screen_state['relics']:
            if relic['name'] == 'Shuriken' and gold >= relic['price']:
                return "shuriken"

        # 3. Membership Card
        for relic in screen_state['relics']:
            if relic['name'] == 'Membership Card' and gold >= relic['price']:
                return "membership card"

        # 4. Shuriken
        for relic in screen_state['relics']:
            if relic['name'] == 'Shuriken' and gold >= relic['price']:
                return "shuriken"

        # 5. Cards based on list
        deck_card_list = state.get_deck_card_list()
        for p in self.cards:
            for card in screen_state['cards']:
                if card['id'] == p and gold >= card['price']:
                    if p.lower not in deck_card_list:
                        return card['name'].lower()

        # 6. Relics based on list
        for p in self.relics:
            for relic in screen_state['relics']:
                if relic['name'] == p and gold >= relic['price']:
                    return relic['name'].lower()

        # 7. Purge in general
        # Would be nicer to not duplicate the list from purge_handler.py here but oh well.
        if can_purge and state.deck.contains_cards([
            'strike',
            'defend',
            'strike+',
            'defend+',
        ]):
            return "purge"


        # Nothing we want / can afford, leave.
        return ''
