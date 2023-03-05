from typing import Callable

from rs.calculator.cards import get_card, CardId
from rs.calculator.interfaces_for_hooks import CardEffectsInterface, HandStateInterface
from rs.calculator.powers import PowerId

CardEffectCustomHook = Callable[[HandStateInterface, CardEffectsInterface, int], None]


def dropkick_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.VULNERABLE):
            state.player.energy += 1
            state.draw_cards(1)


def entrench_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.player.block *= 2


def feed_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __feed_post_hook(state, target_index, 3)


def feed_upgraded_post_hook(state: HandStateInterface, target_index: int = -1):
    __feed_post_hook(state, target_index, 4)


def __feed_post_hook(state: HandStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].current_hp <= 0:
        state.player.max_hp += amount
        state.player.current_hp += amount


def fiend_fire_pre_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    effect.hits = len(state.hand) - 1


def fiend_fire_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    while state.hand:
        state.exhaust_pile.append(state.hand.pop())


def immolate_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.discard_pile.append(get_card(CardId.BURN))


def jax_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] += 2
    else:
        state.player.powers[PowerId.STRENGTH] = 2


def jax_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] += 3
    else:
        state.player.powers[PowerId.STRENGTH] = 3


def limit_break_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] *= 2


def wild_strike_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_pile.append(get_card(CardId.WOUND))


def reckless_charge_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_pile.append(get_card(CardId.DAZED))


def power_through_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    # this is hacky, we should actually have a way of drawing specific cards and overflowing...
    hand_amount = min(2, 10 - len(state.hand))
    discard_amount = 2 - hand_amount
    for i in range(hand_amount):
        state.hand.append(get_card(CardId.WOUND))
    for i in range(discard_amount):
        state.discard_pile.append(get_card(CardId.WOUND))


def spot_weakness_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 3)


def spot_weakness_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 4)


def __spot_weakness_post_hook(state: HandStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].hits:
        if not state.player.powers.get(PowerId.STRENGTH):
            state.player.powers[PowerId.STRENGTH] = 0
        state.player.powers[PowerId.STRENGTH] += amount


def reaper_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if hasattr(effect, 'hp_damage'):
        state.player.heal(effect.hp_damage)


def apotheosis_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    for i in range(len(state.draw_pile)):
        c = state.draw_pile[i]
        state.draw_pile[i] = get_card(c.id, upgrade=c.upgrade + 1)


def blade_dance_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    # this is hacky, we should actually have a way of drawing specific cards and overflowing...
    shiv_amount = 3
    hand_after_blade_dance = max(0, len(state.hand) - 1)
    available_shivs = min(3, 10 - hand_after_blade_dance)
    not_available_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(not_available_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))
    print("Hand count in hook:", len(state.hand))
    print("Discard count in hook:", len(state.discard_pile))


def blade_dance_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    # this is hacky, we should actually have a way of drawing specific cards and overflowing...
    shiv_amount = 4
    hand_after_blade_dance = len(state.hand) - 1
    available_shivs = 10 - hand_after_blade_dance
    not_available_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(not_available_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))


def cloak_and_dagger_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    shiv_amount = 1
    hand_after_blade_dance = len(state.hand) - 1
    available_shivs = 10 - hand_after_blade_dance
    not_available_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(not_available_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))


def cloak_and_dagger_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    shiv_amount = 2
    hand_after_blade_dance = len(state.hand) - 1
    available_shivs = 10 - hand_after_blade_dance
    not_available_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(not_available_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))