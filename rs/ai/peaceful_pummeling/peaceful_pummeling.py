from typing import List

from rs.ai.peaceful_pummeling.config import CARD_REMOVAL_PRIORITY_LIST, HIGH_PRIORITY_UPGRADES, DESIRED_POTIONS, \
    DESIRED_CARDS_FOR_DECK
from rs.ai.peaceful_pummeling.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.peaceful_pummeling.handlers.card_reward_handler import CardRewardHandler
from rs.ai.peaceful_pummeling.handlers.event_handler import EventHandler
from rs.ai.peaceful_pummeling.handlers.neow_handler import NeowHandler
from rs.ai.peaceful_pummeling.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, PotionsEliteHandler
from rs.ai.peaceful_pummeling.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.peaceful_pummeling.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler
from rs.common.handlers.common_mass_discard_handler import CommonMassDiscardHandler
from rs.common.handlers.common_map_handler import CommonMapHandler
from rs.common.handlers.common_purge_handler import CommonPurgeHandler
from rs.common.handlers.common_scry_handler import CommonScryHandler
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler
from rs.common.handlers.common_transform_handler import CommonTransformHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

peaceful_pummeling_potion_handlers: List[Handler] = [
    PotionsBossHandler(),
    # PotionsEventFightHandler(),  # Watcher doesn't really need this one - better to save our potions for the boss.
    PotionsEliteHandler(),
]

PEACEFUL_PUMMELING: AiStrategy = AiStrategy(
    name='PEACEFUL_PUMMELING',
    character=Character.WATCHER,
    handlers=peaceful_pummeling_potion_handlers + [
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonBattleHandler(),
        BossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonCombatRewardHandler(desired_potions=DESIRED_POTIONS),
        CardRewardHandler(),
        NeowHandler(),
        EventHandler(removal_priority_list=CARD_REMOVAL_PRIORITY_LIST, cards_desired_for_deck=DESIRED_CARDS_FOR_DECK),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(HIGH_PRIORITY_UPGRADES, CARD_REMOVAL_PRIORITY_LIST),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonMassDiscardHandler(),
        CommonScryHandler(),
    ]
)
