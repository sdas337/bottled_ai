from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

cards_to_purge: list[str] = ['Conjure blade', 'Conjure blade+', 'Vault', 'Vault+', 'Omniscience',
                             'Omniscience+', 'Meditate', 'Meditate+', 'Defend', 'Strike', 'Wish', 'Wish+', 'Defend+', 'Strike+']


class ShopPurchaseHandler(Handler):

    def __init__(self):
        self.relics = [
            'Bag of Marbles',
            'Pen Nib',
            'Damaru',
            'Shuriken',
            'Red Skull',
            'Preserved Insect',
            'Meat on the Bone',
            'Eternal Feather',
            'Regal Pillow',
            'Lee’s Waffle',
            'Meal Ticket',
            'Strawberry',
            'Strike Dummy',
            'Toy Ornithopter',
            'Pantograph',
            'Pear',
            'Anchor',
            'Horn Cleat',
            'Self-Forming Clay',
            'Thread and Needle',
            'Lantern',
            'Happy Flower',
            'Bag of Preparation',
            'Centennial Puzzle',
        ]

        self.cards = [
            "Tranquility",
            "Crescendo",
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.SHOP_SCREEN.value

    def handle(self, state: GameState) -> HandlerAction:
        choice = self.find_choice(state)
        if choice:
            idx = state.get_choice_list().index(choice)
            if presentation_mode:
                return HandlerAction(commands=[p_delay, "choose " + str(idx), p_delay_s, "wait 30"])
            return HandlerAction(commands=["choose " + str(idx), "wait 30"])
        if presentation_mode:
            return HandlerAction(commands=["wait " + p_delay, "return", "proceed"])
        return HandlerAction(commands=["return", "proceed"])

    def find_choice(self, state: GameState) -> str:
        gold = state.game_state()['gold']
        screen_state = state.game_state()['screen_state']
        can_purge = screen_state['purge_available'] and gold >= screen_state['purge_cost']

        # 1. Purge curses
        if can_purge and state.deck.contains_curses():
            return "purge"

        # 2. Membership Card
        for relic in screen_state['relics']:
            if relic['name'] == 'Membership Card' and gold >= relic['price']:
                return "membership card"

        # 3. Relics based on list
        for p in self.relics:
            for relic in screen_state['relics']:
                if relic['name'] == p and gold >= relic['price']:
                    return relic['name'].lower()

        # 4. Purge in general
        if can_purge and state.deck.contains_cards(cards_to_purge):
            return "purge"

        # 5. Cards based on list
        deck_card_list = state.get_deck_card_list()
        for p in self.cards:
            for card in screen_state['cards']:
                if card['id'] == p and gold >= card['price']:
                    if p.lower not in deck_card_list:
                        return card['name'].lower()

        # Nothing we want / can afford, leave.
        return ''
